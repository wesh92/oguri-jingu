# Supabase CDN/Storage Client

The `image_upload.py` utility here makes use of the supabase python client to upload images from the `data/meta/*` directories into representative directories on supabase.

NOTE: You MUST have images already present in the `data/meta/` directories. Nothing will be uploaded except out of those directories.

## Checklist

- [ ] Bucket "uma_assets" is created or you've changed the name on your supabase project.
- [ ] You have assets to upload in `data/meta`
- [ ] The assets are `.png` or you've updated the MIME type in the image upload client script.
- [ ] !IMPORTANT: The directory structure under `data/meta` is _exactly_ the structure you want to use on supabase. By default this would be like `/(region)/(category)/(asset_name).png`.
