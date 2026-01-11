# SEO & Indexing Fix Plan - ConvertRocket

## Issues Identified

### 1. Server 5xx Errors
- https://www.convertrocket.online/blog/pdf-to-excel
- https://www.convertrocket.online/?ref=producthunt
- https://convertrocket.online/blog/top-5-youtube-downloaders-2025/
- https://www.convertrocket.online/index.html
- https://www.convertrocket.online/blog/pdf-to-word-guide-students
- https://www.convertrocket.online/blogs.html
- https://www.convertrocket.online/docs/oauth2-redirect

### 2. Pages with Redirects (Need proper 301)
- https://www.convertrocket.online/pdf-to-excel.html → /pdf-to-excel
- http://convertrocket.online/ → https://www.convertrocket.online/
- https://convertrocket.online/ → https://www.convertrocket.online/
- http://www.convertrocket.online/ → https://www.convertrocket.online/

### 3. Duplicate Without Canonical
- https://www.convertrocket.online/pdf-to-excel/
- https://www.convertrocket.online/image-converter.html

### 4. 301 Moved Permanently (Non-www to www)
All tool pages need proper redirects from non-www to www

### 5. Discovered/Crawled but Not Indexed
- Blog posts not loading correctly
- openapi.json issues

## Fix Strategy

### Phase 1: Backend Routing Fixes
1. Add www redirect middleware
2. Fix all missing routes
3. Add trailing slash normalization
4. Handle query parameters properly

### Phase 2: Sitemap Updates
1. Update all URLs to www.convertrocket.online
2. Add missing pages
3. Update lastmod dates
4. Add all blog posts

### Phase 3: Frontend Updates
1. Add canonical tags to all pages
2. Fix navigation links
3. Update meta tags
4. Add structured data

### Phase 4: Design & UX Improvements
1. Ultra-modern UI redesign
2. Add 3D elements
3. Improve interactivity
4. Fix tab appearance consistency
5. Add visual effects
6. Ensure AI tools work properly

## Status
- [ ] Phase 1: Backend Routing
- [ ] Phase 2: Sitemap Updates
- [ ] Phase 3: Frontend Updates
- [ ] Phase 4: Design Improvements
