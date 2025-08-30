# Music Producer Website

A professional Flask-based website for music producers featuring portfolio showcase, booking system, and client management.

## Features

- **Professional Homepage** - Showcase your work and services
- **Portfolio Gallery** - Display your beats and tracks with audio players
- **Booking System** - Allow clients to book sessions online
- **Contact Forms** - Easy communication with potential clients
- **Responsive Design** - Works on all devices
- **Email Integration** - Automated notifications for bookings and contacts

## Setup Instructions

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Project Structure

Create the following folder structure:

```
music_producer_website/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/            # HTML templates
│   ├── base.html
│   ├── home.html
│   ├── portfolio.html
│   ├── book.html
│   ├── contact.html
│   ├── services.html
│   └── about.html
├── static/               # Static files
│   ├── uploads/          # For audio files
│   ├── css/             # Custom CSS (optional)
│   └── js/              # Custom JavaScript (optional)
└── README.md
```

### 3. Email Configuration

Update the email settings in `app.py`:

```python
# Replace with your email settings
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your-app-password'  # Use App Password for Gmail
```

For Gmail:
1. Enable 2-factor authentication
2. Generate an "App Password" in your Google Account settings
3. Use the app password instead of your regular password

### 4. Customize Your Information

Edit the following in your templates:

- **Producer Name**: Replace "ProducerName" throughout the templates
- **Contact Information**: Update email, phone, and address in base.html
- **Portfolio**: Update the PORTFOLIO list in app.py with your actual tracks
- **Services**: Modify the SERVICES list with your offerings and pricing
- **Social Links**: Update social media links in the footer

### 5. Audio Files Setup

1. Create the `static/uploads/` directory
2. Add your audio files (MP3, WAV, etc.)
3. Update the `audio_file` field in the PORTFOLIO data to match your file names

### 6. Run the Application

```bash
python app.py
```

The website will be available at `http://localhost:5000`

## Customization

### Adding New Pages

1. Create a new route in `app.py`
2. Create the corresponding HTML template
3. Add navigation links in `base.html`

### Styling

The website uses Bootstrap 5 with custom CSS variables. Modify the CSS variables in `base.html` to change colors:

```css
:root {
    --primary-color: #ff6b6b;      /* Main brand color */
    --secondary-color: #4ecdc4;    /* Accent color */
    --dark-color: #2c3e50;         /* Dark backgrounds */
    --accent-color: #f39c12;       /* Highlights */
}
```

### Database Integration

For production use, consider integrating with a database:

- **SQLite** for simple local storage
- **PostgreSQL** for more robust production deployment
- **MongoDB** for flexible document storage

### Deployment Options

1. **Heroku** - Easy deployment with git
2. **DigitalOcean App Platform** - Simple and affordable
3. **AWS Elastic Beanstalk** - Scalable cloud hosting
4. **Vercel/Netlify** - For static site generation

## Additional Features to Consider

### Phase 2 Enhancements:
- User authentication for client accounts
- Payment integration (Stripe/PayPal)
- File sharing and collaboration tools
- Calendar integration for booking
- Real audio player integration
- Admin dashboard for managing content
- SEO optimization
- Analytics integration

### Audio Player Integration:
Replace the mockup audio players with real functionality using:
- **Howler.js** for web audio
- **WaveSurfer.js** for waveform visualization
- **Plyr** for custom audio controls

## Security Considerations

1. **Environment Variables**: Store sensitive data in environment variables
2. **File Upload Validation**: Implement proper file type and size validation
3. **Rate Limiting**: Add rate limiting to prevent spam
4. **HTTPS**: Always use HTTPS in production
5. **Input Sanitization**: Validate and sanitize all user inputs

## License

This project is open source. Feel free to customize and use for your music production business.