Wari Help Map - Mobile Friendly UI Package

Files
1. wari_help_map_public_mobile.html
   - Public/mobile friendly map for Warkari/general public/Dindi heads.
   - Uses only public-ready points: 29 points.
   - Large buttons, nearest help, call, directions, share current location.

2. wari_help_map_control_room_mobile.html
   - Control room/admin version.
   - Includes all available points: 56 points.
   - Shows public-ready and verification-required points.

Recommended deployment
- Host the public HTML on HTTPS using GitHub Pages, Netlify, Vercel, Sarvaha server, or NHM server.
- Generate QR code for the public URL.
- Keep the control room HTML for internal team only.

Important
- GPS works reliably only on HTTPS or localhost.
- Public version does not show unverified records.
- Add water/toilet/food/helpdesk data later using same CSV format.
