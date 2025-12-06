"""
Test ConvertRocket Conversions
Tests all working conversions to verify deployment readiness
"""

import requests
import os
from pathlib import Path

BASE_URL = "http://localhost:8000"

def test_health():
    """Test if server is running"""
    try:
        r = requests.get(f"{BASE_URL}/api/health")
        if r.status_code == 200:
            print("✅ Server is running")
            return True
        else:
            print(f"❌ Server returned {r.status_code}")
            return False
    except Exception as e:
        print(f"❌ Server not accessible: {e}")
        return False

def test_formats_endpoint():
    """Test formats endpoint"""
    try:
        r = requests.get(f"{BASE_URL}/api/convert/formats")
        data = r.json()
        print(f"✅ Formats endpoint working - {len(data['formats'])} categories")
        return True
    except Exception as e:
        print(f"❌ Formats endpoint failed: {e}")
        return False

def test_image_conversion():
    """Test image conversion (should work without FFmpeg)"""
    try:
        # Create a simple test image
        from PIL import Image
        
        test_dir = Path("test_files")
        test_dir.mkdir(exist_ok=True)
        
        # Create test PNG
        img = Image.new('RGB', (100, 100), color='red')
        test_png = test_dir / "test.png"
        img.save(test_png)
        
        # Test PNG to JPEG conversion
        with open(test_png, 'rb') as f:
            files = {'file': ('test.png', f, 'image/png')}
            data = {'target_format': 'jpeg'}
            r = requests.post(f"{BASE_URL}/api/convert/upload", files=files, data=data)
        
        result = r.json()
        if result.get('success'):
            print(f"✅ Image conversion working: PNG → JPEG")
            print(f"   Original: {result.get('original_file')}")
            print(f"   Converted: {result.get('converted_file')}")
            return True
        else:
            print(f"❌ Image conversion failed: {result.get('message')}")
            return False
            
    except Exception as e:
        print(f"❌ Image conversion test error: {e}")
        return False
    finally:
        # Cleanup
        if test_png.exists():
            test_png.unlink()
        if test_dir.exists():
            test_dir.rmdir()

def test_document_conversion():
    """Test document conversion"""
    try:
        from docx import Document
        
        test_dir = Path("test_files")
        test_dir.mkdir(exist_ok=True)
        
        # Create test DOCX
        doc = Document()
        doc.add_paragraph("Test document for ConvertRocket")
        test_docx = test_dir / "test.docx"
        doc.save(test_docx)
        
        # Test DOCX to TXT conversion
        with open(test_docx, 'rb') as f:
            files = {'file': ('test.docx', f, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')}
            data = {'target_format': 'txt'}
            r = requests.post(f"{BASE_URL}/api/convert/upload", files=files, data=data)
        
        result = r.json()
        if result.get('success'):
            print(f"✅ Document conversion working: DOCX → TXT")
            print(f"   Converted: {result.get('converted_file')}")
            return True
        else:
            print(f"❌ Document conversion failed: {result.get('message')}")
            return False
            
    except Exception as e:
        print(f"❌ Document conversion test error: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Cleanup
        if test_docx.exists():
            test_docx.unlink()
        if test_dir.exists() and not list(test_dir.iterdir()):
            test_dir.rmdir()

def main():
    print("=" * 60)
    print("🚀 ConvertRocket - Deployment Tests")
    print("=" * 60)
    print()
    
    results = []
    
    # Test 1: Server Health
    print("1. Testing Server Health...")
    results.append(("Server Health", test_health()))
    print()
    
    # Test 2: Formats Endpoint
    print("2. Testing Formats Endpoint...")
    results.append(("Formats API", test_formats_endpoint()))
    print()
    
    # Test 3: Image Conversion
    print("3. Testing Image Conversion (PNG → JPEG)...")
    results.append(("Image Conversion", test_image_conversion()))
    print()
    
    # Test 4: Document Conversion
    print("4. Testing Document Conversion (DOCX → TXT)...")
    results.append(("Document Conversion", test_document_conversion()))
    print()
    
    # Summary
    print("=" * 60)
    print("📊 Test Results Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print()
    print(f"Total: {passed}/{total} tests passed")
    print()
    
    if passed == total:
        print("🎉 ALL TESTS PASSED - READY FOR DEPLOYMENT!")
    elif passed >= total - 1:
        print("⚠️  MOSTLY READY - Minor issues detected")
    else:
        print("❌ NOT READY - Multiple failures detected")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
