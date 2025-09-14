from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import datetime, timedelta
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Updated services data based on your rate card
services = [
    {
        'name': 'Single Track Mixing',
        'price': '$550',
        'description': 'Professional mixing for a single track to enhance clarity, depth, and balance. Perfect for singles and individual releases.',
        'features': [
            'EQ balancing and frequency shaping',
            'Dynamic range compression',
            'Spatial effects and reverb',
            'Stereo imaging enhancement',
            'Final export in MP3 and WAV formats',
            '2 revisions included',
            '3-5 day turnaround'
        ]
    },
    {
        'name': 'EP Mixing (3-5 Tracks)',
        'price': '$500 per track',
        'description': 'Complete mixing for an EP with 3-5 tracks at a discounted rate with consistent sonic character.',
        'features': [
            'Consistent sound across all tracks',
            'Bulk discount pricing',
            'Album-style sequencing considerations',
            'Unified sonic character',
            'All formats included',
            '3 revisions per track',
            '1-2 week turnaround'
        ]
    },
    {
        'name': 'Album Mixing (6+ Tracks)',
        'price': '$650 per track',
        'description': 'Professional album mixing with attention to consistency, flow, and mastering preparation.',
        'features': [
            'Album sequencing optimization',
            'Consistent sonic character throughout',
            'Mastering preparation',
            'Detailed track notes',
            'Stems delivery included',
            'Unlimited revisions',
            '2-3 week turnaround'
        ]
    },
    {
        'name': 'Single Track Mastering',
        'price': '$300',
        'description': 'Final polish and loudness optimization for a single track, ready for all streaming platforms.',
        'features': [
            'Loudness optimization for streaming',
            'Final EQ and dynamics processing',
            'Stereo enhancement',
            'Format conversion (MP3, WAV)',
            'Streaming platform compliance',
            '2 revisions included',
            '1-2 day turnaround'
        ]
    },
    {
        'name': 'EP Mastering (3-5 Tracks)',
        'price': '$550 total',
        'description': 'Complete mastering for EP projects with consistent loudness and sonic character across all tracks.',
        'features': [
            'Consistent LUFS across tracks',
            'Album-style mastering approach',
            'Gap timing optimization',
            'All streaming formats',
            'DDP master for CD',
            '3 revisions included',
            '3-5 day turnaround'
        ]
    },
    {
        'name': 'Album Mastering (6+ Tracks)',
        'price': '$1,000 total',
        'description': 'Professional album mastering with attention to flow, dynamics, and commercial standards.',
        'features': [
            'Complete album mastering',
            'Professional sequencing',
            'ISRC code embedding',
            'Multiple format delivery',
            'DDP master included',
            'Unlimited revisions',
            '1-2 week turnaround'
        ]
    },
    {
        'name': 'Beat Production',
        'price': '$400',
        'description': 'Original, high-energy instrumental beats for various genres including Afrobeats, Hip-Hop, Gospel, and R&B.',
        'features': [
            'Original composition and arrangement',
            'Genre-specific production elements',
            'High-quality sound libraries',
            'Basic mixing included',
            'MP3 and WAV delivery',
            'Unlimited revisions',
            '3-5 day turnaround'
        ]
    },
    {
        'name': 'Full Song Production',
        'price': '$800',
        'description': 'Complete song production from concept to final mix, including arrangement and instrumentation.',
        'features': [
            'Complete song arrangement',
            'Professional instrumentation',
            'Vocal arrangement (if applicable)',
            'Full mixing included',
            'Multiple format delivery',
            '3 revisions included',
            '1-2 week turnaround'
        ]
    },
    {
        'name': 'Full Production + Mix & Master',
        'price': '$1,000',
        'description': 'Complete end-to-end production service from concept to radio-ready master.',
        'features': [
            'Complete song production',
            'Professional mixing',
            'Radio-ready mastering',
            'All file formats included',
            'Stems delivery',
            'Unlimited revisions',
            '2-3 week turnaround'
        ]
    },
    {
        'name': 'Recording Session',
        'price': '$50 per hour',
        'description': 'Professional recording sessions in a controlled studio environment with high-quality equipment.',
        'features': [
            'Professional microphones and preamps',
            'Real-time monitoring',
            'Vocal coaching assistance',
            'Take comping and editing',
            'Session files provided',
            'Flexible scheduling',
            'Minimum 2-hour booking'
        ]
    }
]

# Updated portfolio with audio file paths
portfolio = [
    {
        'id': 1,
        'title': 'Another Level',
        'artist': 'Jaywon ft Mr Eazi',
        'genre': 'Afrobeats',
        'duration': '3:45',
        'date': '2024-01-15',
        'description': 'Mixed for Jaywon ft Mr Eazi - a vibrant Afrobeats track with rich instrumentation and dynamic vocals.',
        'link': 'https://youtu.be/duu19n8FIas?si=2AGkI0fXKwE_5EJz',
        'service': 'Mixing',
        'audio_file': 'audio/another_level_preview.mp3'  # Add your audio file path
    },
    {
        'id': 2,
        'title': 'Holy Ghost Air',
        'artist': 'Ty Bello ft Nathaniel Bassey',
        'genre': 'Gospel',
        'duration': '5:20',
        'date': '2024-02-10',
        'description': 'Mixed for Ty Bello ft Nathaniel Bassey - an uplifting gospel worship song with powerful vocals and orchestral arrangements.',
        'link': 'https://youtu.be/NedsBECzoto?si=VeT36WKkxpll_Z1L',
        'service': 'Mixing',
        'audio_file': 'audio/holy_ghost_air_preview.mp3'
    },
    {
        'id': 3,
        'title': 'EDiV Track',
        'artist': 'EDiV',
        'genre': 'Hip-Hop',
        'duration': '3:15',
        'date': '2024-03-05',
        'description': 'Produced and mixed for EDiV - a hard-hitting hip-hop track with clean vocals and punchy drums.',
        'link': 'https://youtu.be/69loIV8GUnI?si=qRa7_bKrrL_j2kJ5',
        'service': 'Production + Mixing',
        'audio_file': 'audio/ediv_track_preview.mp3'
    },
    {
        'id': 4,
        'title': 'Falz Track',
        'artist': 'Falz',
        'genre': 'Afrobeats',
        'duration': '3:30',
        'date': '2024-01-28',
        'description': 'Mixed for Falz - a catchy Afrobeats track with clever wordplay and modern production elements.',
        'link': 'https://youtu.be/vCpaqzCz_jc?si=aS9S4n1HT6DDj0AS',
        'service': 'Mixing',
        'audio_file': 'audio/falz_track_preview.mp3'
    },
    {
        'id': 5,
        'title': 'Ojekunle Track',
        'artist': 'Ojekunle',
        'genre': 'Gospel',
        'duration': '4:15',
        'date': '2024-02-20',
        'description': 'Mixed for Ojekunle - a soulful gospel track with powerful vocals and inspiring message.',
        'link': 'https://youtu.be/IquTmJRUTsM?si=H72hZjdMEa7znzmO',
        'service': 'Mixing',
        'audio_file': 'audio/ojekunle_track_preview.mp3'
    },
    {
        'id': 6,
        'title': 'Thank You',
        'artist': 'Minister Kenn',
        'genre': 'Gospel',
        'duration': '4:45',
        'date': '2024-03-12',
        'description': 'Mixed for Minister Kenn - a heartfelt gospel worship song with rich harmonies.',
        'link': 'https://youtu.be/iPlx36Gj6FI?si=PBGfD16PUdIgmdb0',
        'service': 'Mixing',
        'audio_file': 'audio/thank_you_preview.mp3'
    },
    {
        'id': 7,
        'title': 'EDiV Track 2',
        'artist': 'EDiV',
        'genre': 'Hip-Hop',
        'duration': '3:35',
        'date': '2024-03-20',
        'description': 'Another collaboration with EDiV featuring crisp vocals and modern hip-hop production.',
        'link': 'https://youtu.be/fQHDgIT3f4Y?si=bFpY_AvSBLzhabVu',
        'service': 'Mixing & Mastering',
        'audio_file': 'audio/ediv_track2_preview.mp3'
    },
    {
        'id': 8,
        'title': 'Press Play',
        'artist': 'Mbithi',
        'genre': 'Afrobeats',
        'duration': '3:50',
        'date': '2024-04-01',
        'description': 'Complete production, mixing and mastering for Mbithi - an energetic Afrobeats anthem.',
        'link': 'https://youtu.be/3byFvvnQmek?si=f8JQmDlScxRgvdsJ',
        'service': 'Full Production + Mix & Master',
        'audio_file': 'audio/press_play_preview.mp3'
    },
    {
        'id': 9,
        'title': 'Sporedust Media Soundtrack',
        'artist': 'Various',
        'genre': 'Soundtrack',
        'duration': '2:30',
        'date': '2024-04-15',
        'description': 'Audio cleaning and enhancement for Sporedust Media - professional podcast and media audio processing.',
        'link': 'https://youtu.be/9tI8RfN2iTA?si=XNH-BsV-NEneEVGl',
        'service': 'Audio Cleaning',
        'audio_file': 'audio/sporedust_soundtrack_preview.mp3'
    }
]

# Updated testimonials with your actual client feedback
testimonials = [
    {
        'name': 'Jaywon ft Mr Eazi',
        'text': 'Another Level was well Mixed!',
        'link': 'https://youtu.be/duu19n8FIas?si=2AGkI0fXKwE_5EJz',
        'project': 'Another Level'
    },
    {
        'name': 'EDiV',
        'text': 'JazzyMix took my raw track and transformed it into something truly professional. His attention to detail is unmatched!',
        'link': 'https://youtu.be/69loIV8GUnI?si=qRa7_bKrrL_j2kJ5',
        'project': 'Hip-Hop Track'
    },
    {
        'name': 'Ty Bello ft Nathaniel Bassey',
        'text': 'Ty Bello ft Nathaniel Bassey\'s \'Holy Ghost Air\' reached new heights with JazzyMix!',
        'link': 'https://youtu.be/NedsBECzoto?si=VeT36WKkxpll_Z1L',
        'project': 'Holy Ghost Air'
    },
    {
        'name': 'Falz',
        'text': 'Falz\'s track was a job well done with JazzyMix!',
        'link': 'https://youtu.be/vCpaqzCz_jc?si=aS9S4n1HT6DDj0AS',
        'project': 'Afrobeats Track'
    },
    {
        'name': 'Ojekunle',
        'text': 'Ojekunle track resonated deeply with JazzyMix mixing and mastering!',
        'link': 'https://youtu.be/IquTmJRUTsM?si=H72hZjdMEa7znzmO',
        'project': 'Gospel Track'
    },
    {
        'name': 'Minister Kenn',
        'text': 'Thank You was executed perfectly by JazzyMix mixing and mastering!',
        'link': 'https://youtu.be/iPlx36Gj6FI?si=PBGfD16PUdIgmdb0',
        'project': 'Thank You'
    },
    {
        'name': 'Mbithi',
        'text': 'Mbithi Press Play became a favorite after JazzyMix production, mixing and mastering!',
        'link': 'https://youtu.be/3byFvvnQmek?si=f8JQmDlScxRgvdsJ',
        'project': 'Press Play'
    },
    {
        'name': 'Sporedust Media',
        'text': 'Our soundtrack has never sounded better thanks to his audio cleaning services. Highly recommend him!',
        'link': 'https://youtu.be/9tI8RfN2iTA?si=XNH-BsV-NEneEVGl',
        'project': 'Media Soundtrack'
    }
]

# Updated genres list
genres = ['All', 'Afrobeats', 'Hip-Hop', 'Gospel', 'R&B', 'Pop', 'Soundtrack']

# Recent work for homepage (latest 3 tracks)
recent_work = [
    {
        'title': 'Press Play',
        'genre': 'Afrobeats',
        'duration': '3:50',
        'date': 'Apr 2024',
        'description': 'Complete production for Mbithi - energetic Afrobeats with modern production elements.'
    },
    {
        'title': 'Sporedust Media Soundtrack',
        'genre': 'Soundtrack',
        'duration': '2:30',
        'date': 'Apr 2024',
        'description': 'Professional audio cleaning and enhancement for media content.'
    },
    {
        'title': 'Thank You',
        'genre': 'Gospel',
        'duration': '4:45',
        'date': 'Mar 2024',
        'description': 'Mixed for Minister Kenn - heartfelt gospel worship with rich harmonies.'
    }
]

@app.route('/')
def home():
    return render_template('home.html', 
                         services=services[:4],  # Show first 4 services
                         recent_work=recent_work, 
                         testimonials=testimonials[:4])  # Show first 4 testimonials

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/portfolio')
def portfolio_page():
    genre_filter = request.args.get('genre', 'all').lower()
    
    if genre_filter == 'all':
        filtered_portfolio = portfolio
    else:
        filtered_portfolio = [work for work in portfolio if work['genre'].lower() == genre_filter]
    
    return render_template('portfolio.html', 
                         portfolio=filtered_portfolio, 
                         genres=genres, 
                         current_genre=genre_filter)

@app.route('/services')
def services_page():
    return render_template('services.html', services=services)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Process form data
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        # Here you would typically save this to a database or send an email
        # For now, we'll just flash a success message
        flash(f'Thank you {name}! Your message has been received. I will get back to you within 24 hours.', 'success')
        return redirect(url_for('contact'))
    
    return render_template('contact.html')

@app.route('/book', methods=['GET', 'POST'])
def book():
    if request.method == 'POST':
        # Process booking form
        name = request.form.get('name')
        email = request.form.get('email')
        service = request.form.get('service')
        date = request.form.get('date')
        time = request.form.get('time')
        description = request.form.get('description')
        phone = request.form.get('phone')
        budget = request.form.get('budget')
        
        # Here you would typically save this to a database and send confirmation emails
        flash(f'Thank you {name}! Your session for {service} on {date} at {time} has been booked. I will send a confirmation email shortly with next steps.', 'success')
        return redirect(url_for('book'))
    
    return render_template('book.html', services=services)

@app.route('/admin')
def admin_login():
    """Admin login page"""
    return render_template('adminlog.html')

@app.route('/admin/login', methods=['POST'])
def admin_login_post():
    """Handle admin login form submission"""
    username = request.form.get('username')
    password = request.form.get('password')
    
    # In a real application, you'd verify credentials against a database
    if username == 'jazzymix_admin' and password == 'Jesuschrist1!':
        # Set session variables to track login
        session['admin_logged_in'] = True
        session['admin_username'] = username
        flash('Login successful! Welcome to the admin panel.', 'success')
        return redirect(url_for('admin_dashboard'))
    else:
        flash('Invalid credentials. Please try again.', 'error')
        return redirect(url_for('admin_login'))

@app.route('/admin/dashboard')
def admin_dashboard():
    """Admin dashboard/panel"""
    # Check if user is logged in
    if not session.get('admin_logged_in'):
        flash('Please log in to access the admin panel.', 'error')
        return redirect(url_for('admin_login'))
    
    return render_template('adminpanel.html')

@app.route('/admin/logout')
def admin_logout():
    """Admin logout"""
    session.pop('admin_logged_in', None)
    session.pop('admin_username', None)
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('home'))

# Optional: Add a route to check admin status
@app.route('/admin/status')
def admin_status():
    """Check admin login status (for AJAX calls)"""
    from flask import jsonify
    return jsonify({
        'logged_in': session.get('admin_logged_in', False),
        'username': session.get('admin_username', '')
    })

@app.route('/api/availability/<date>')
def check_availability(date):
    """
    Mock availability API - in a real app, you'd check against a database
    Returns available time slots for a given date
    """
    try:
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        
        # Business hours: 8 AM - 10 PM weekdays, 10 AM - 8 PM weekends
        if date_obj.weekday() < 5:  # Monday to Friday
            available_times = [
                '10:00 AM', '11:00 AM', '12:00 PM', '1:00 PM', '2:00 PM', 
                '3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM', '7:00 PM', 
                '8:00 PM', '9:00 PM'
            ]
        else:  # Saturday or Sunday
            available_times = [
                '12:00 PM', '1:00 PM', '2:00 PM', '3:00 PM', 
                '4:00 PM', '5:00 PM', '6:00 PM', '7:00 PM'
            ]
        
        # Remove some slots randomly to simulate bookings
        import random
        if random.random() > 0.3:  # 70% chance of full availability
            available_times = available_times[::2]  # Take every other slot
            
        return {'available': True, 'times': available_times}
        
    except ValueError:
        return {'available': False, 'times': [], 'error': 'Invalid date format'}

@app.route('/index')
def index():
    """Route to the original index page"""
    return render_template('index.html')

# Additional routes for SEO and user experience
@app.route('/mixing')
def mixing_service():
    """Dedicated page for mixing services"""
    mixing_services = [s for s in services if 'mixing' in s['name'].lower()]
    return render_template('services.html', services=mixing_services, page_title="Professional Mixing Services")

@app.route('/mastering') 
def mastering_service():
    """Dedicated page for mastering services"""
    mastering_services = [s for s in services if 'mastering' in s['name'].lower()]
    return render_template('services.html', services=mastering_services, page_title="Professional Mastering Services")

@app.route('/beats')
def beats_service():
    """Dedicated page for beat production"""
    beat_services = [s for s in services if 'beat' in s['name'].lower() or 'production' in s['name'].lower()]
    return render_template('services.html', services=beat_services, page_title="Original Beat Production")

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

# Template filters
@app.template_filter('currency')
def currency_filter(value):
    """Format currency values"""
    if isinstance(value, str) and '$' in value:
        return value
    return f"${value}"

# Context processors (make data available to all templates)
@app.context_processor
def inject_globals():
    return {
        'current_year': datetime.now().year,
        'site_name': 'JazzyMix',
        'producer_name': 'Agualomunu Samson Seun',
        'contact_email': 'psalmjazzymix001@yahoo.com',
        'contact_phone': '+254 111 925802',
        'instagram': 'https://instagram.com/jazzy.mix',
        'location': 'Nairobi, Kenya'
    }

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)