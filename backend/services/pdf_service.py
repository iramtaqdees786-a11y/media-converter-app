import os
from pathlib import Path
from typing import List, Optional
import pypdf
from pypdf import PdfReader, PdfWriter

class PDFService:
    def __init__(self, upload_dir: Path, converted_dir: Path):
        self.upload_dir = upload_dir
        self.converted_dir = converted_dir

    async def merge_pdfs(self, file_paths: List[Path], output_filename: str) -> Path:
        """Merge multiple PDFs into one."""
        merger = pypdf.PdfWriter()
        
        for path in file_paths:
            merger.append(path)

        output_path = self.converted_dir / output_filename
        with open(output_path, "wb") as f_out:
            merger.write(f_out)
            
        merger.close()
        return output_path

    async def remove_pages(self, file_path: Path, pages_to_remove: List[int], output_filename: str) -> Path:
        """Remove specific pages from a PDF. Pages are 1-indexed."""
        reader = PdfReader(file_path)
        writer = PdfWriter()
        
        # Convert 1-indexed to 0-indexed for internal use
        pages_to_remove_0 = [p - 1 for p in pages_to_remove]
        
        for i, page in enumerate(reader.pages):
            if i not in pages_to_remove_0:
                writer.add_page(page)

        output_path = self.converted_dir / output_filename
        with open(output_path, "wb") as f_out:
            writer.write(f_out)
            
        return output_path

    async def compress_pdf(self, file_path: Path, output_filename: str) -> Path:
        """
        Compress PDF using Ghostscript if available, otherwise fallback to pypdf.
        """
        output_path = self.converted_dir / output_filename
        
        # Try finding gs
        gs_names = ["gswin64c", "gswin32c", "gs"]
        gs_exe = None
        from shutil import which
        for name in gs_names:
            if which(name):
                gs_exe = name
                break
        
        if gs_exe:
            try:
                import subprocess
                # Using -dPDFSETTINGS=/ebook for a good balance of quality and size
                subprocess.run([
                    gs_exe,
                    "-sDEVICE=pdfwrite",
                    "-dCompatibilityLevel=1.4",
                    "-dPDFSETTINGS=/ebook",
                    "-dNOPAUSE",
                    "-dQUIET",
                    "-dBATCH",
                    "-sOutputFile=" + str(output_path),
                    str(file_path)
                ], check=True)
                return output_path
            except Exception as e:
                print(f"Ghostscript compression failed: {e}")

        # Fallback to pypdf
        reader = PdfReader(file_path)
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        for page in writer.pages:
            page.compress_content_streams() 

        writer.compress_identical_objects(remove_identicals=True, remove_identical_objects=True) 

        with open(output_path, "wb") as f_out:
            writer.write(f_out)
            
        return output_path

    async def grayscale_pdf(self, file_path: Path, output_filename: str) -> Path:
        """
        Convert to Grayscale. 
        PyPDF doesn't support direct color conversion easily.
        A robust way requires ghostscript or converting pages to images and back.
        We'll try a simple method if possible, otherwise I might need to skip or warn.
        
        Actually, for a high quality grayscale, using Ghostscript is best.
        Since I cannot rely on GS, I will implement a "PDF to Images (Grayscale) to PDF" method
        using pdf2image (needs poppler) + PIL.
        
        Wait, `pdf2image` needs poppler. `pypdf` alone can't really do this.
        Check if we have poppler. If not, this feature is hard.
        
        Let's try a different approach: Metadata modification? No.
        
        Alternative: Iterate over content streams and replace color operators? Very risky.
        
        Let's implement a placeholder that warns or attempts to use 'ghostscript' via subprocess if found.
        """
        # Placeholder for now, or check for ghostscript
        import subprocess
        output_path = self.converted_dir / output_filename
        
        # Try finding gs
        gs_names = ["gswin64c", "gswin32c", "gs"]
        gs_exe = None
        for name in gs_names:
            from shutil import which
            if which(name):
                gs_exe = name
                break
        
        if gs_exe:
             # gs -sDEVICE=pdfwrite -sProcessColorModel=DeviceGray -sColorConversionStrategy=Gray -dOverrideICC -o out.pdf in.pdf
            try:
                subprocess.run([
                    gs_exe, 
                    "-sDEVICE=pdfwrite", 
                    "-sProcessColorModel=DeviceGray", 
                    "-sColorConversionStrategy=Gray", 
                    "-dOverrideICC", 
                    "-o", str(output_path), 
                    str(file_path)
                ], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                return output_path
            except Exception as e:
                print(f"GS failed: {e}")
                pass

        # Fallback: Just return original or raise error?
        # Let's try to just return the original with a "Failed to convert" log for now 
        # OR implement Image conversion if we had poppler.
        # Given limitations, I will remove this from "Implementation" code for now or make it a pass-through.
        # But user requested it. I will leave the GS attempt.
        
        raise NotImplementedError("Grayscale conversion requires Ghostscript installed on the server.")

    async def convert_to_pdfa(self, file_path: Path, output_filename: str) -> Path:
        import subprocess
        output_path = self.converted_dir / output_filename
        
        # Try finding gs
        gs_names = ["gswin64c", "gswin32c", "gs"]
        gs_exe = None
        for name in gs_names:
            from shutil import which
            if which(name):
                gs_exe = name
                break

        if gs_exe:
            # Simple PDF/A-1b conversion (requires specific color profile, usually pdftocairo or gs)
            # This is complex without a PDFA_def.ps file.
            # Simplified version:
            try:
                subprocess.run([
                    gs_exe,
                    "-dPDFA=2",
                    "-dBATCH",
                    "-dNOPAUSE",
                    "-sProcessColorModel=DeviceCMYK",
                    "-sDEVICE=pdfwrite",
                    "-sPDFACompatibilityPolicy=1",
                    "-o", str(output_path),
                    str(file_path)
                ], check=True)
                return output_path
            except Exception as e:
                pass
        
        raise NotImplementedError("PDF/A conversion requires Ghostscript.")
