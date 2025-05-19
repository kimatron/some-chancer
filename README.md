Some Chancer - Modern Raffle Platform
Show Image
A sleek, modern raffle platform that lets users purchase tickets for exciting prize draws with a distinctive visual style inspired by hand-drawn, sketchy aesthetics.
🎮 Live Demo
somechancer.com - Coming Soon!
✨ Features

Bold, Distinctive Design: Eye-catching UI with animated elements, sketchy borders, and playful interactions
Dynamic Raffle System: Create and manage raffles with configurable ticket quantities and prices
Secure Payment Processing: Integrated with Stripe for safe, reliable transactions
User Accounts: Personal dashboards to track tickets, winnings, and account details
Transparent Winner Selection: Fair and verifiable random selection process
Responsive Layout: Seamless experience across mobile, tablet, and desktop devices
Real-time Updates: Live ticket counters and time-remaining displays
Email Notifications: Automated messages for purchases, winnings, and important updates

🖼️ Screenshots
<div style="display: flex; flex-wrap: wrap; gap: 10px; justify-content: center;">
    <img src="https://via.placeholder.com/400x250/4876ff/ffffff?text=Homepage" alt="Homepage" width="400"/>
    <img src="https://via.placeholder.com/400x250/ff7347/ffffff?text=Raffle+Details" alt="Raffle Details" width="400"/>
    <img src="https://via.placeholder.com/400x250/692e54/ffffff?text=User+Dashboard" alt="User Dashboard" width="400"/>
    <img src="https://via.placeholder.com/400x250/d9f154/333333?text=Winners+Gallery" alt="Winners Gallery" width="400"/>
</div>
🛠️ Tech Stack

Backend: Django 5.2, Python 3.12
Frontend: HTML5, CSS3, JavaScript
Styling: Bootstrap 5, Custom CSS with fluid typography
Database: PostgreSQL
Payment Processing: Stripe API
Caching: Redis
Task Queue: Django-Q
Deployment: Docker, Nginx, Gunicorn

🚀 Getting Started
Prerequisites

Python 3.10+
PostgreSQL
Redis
Stripe account

Installation

Clone the repository
bashgit clone https://github.com/yourusername/some-chancer.git
cd some-chancer

Create and activate a virtual environment
bashpython -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install dependencies
bashpip install -r requirements.txt

Set up environment variables
bashcp .env.example .env
# Edit .env with your configuration

Run migrations
bashpython manage.py migrate

Create a superuser
bashpython manage.py createsuperuser

Start the development server
bashpython manage.py runserver

Visit http://127.0.0.1:8000/ in your browser

🌟 Usage
Admin Panel

Navigate to http://127.0.0.1:8000/admin/
Log in with your superuser credentials
Create and manage raffles, view transactions, and more

Creating a Raffle

From the admin panel, go to "Raffles" > "Add Raffle"
Fill in all required fields:

Title and description
Upload an image
Set ticket price and total tickets
Configure start and end dates
Toggle "Featured" for homepage promotion


Save the raffle

Drawing a Winner

When a raffle ends, log in as an admin
Navigate to the raffle detail page
Click "Draw Winner" to randomly select from purchased tickets
The system will automatically notify the winner

💡 Design Inspiration
The distinctive aesthetic of Some Chancer draws inspiration from hand-drawn sketches and modern web design trends. Key elements include:

SVG Filters: Creating the "squiggly" hand-drawn effect on borders and images
Fluid Typography: Responsive text sizing that scales perfectly across devices
Animated Effects: Subtle animations that bring the interface to life
Custom Buttons: Distinctive, playful button styles with hover effects
Bold Color Palette: Vibrant colors that create visual interest and guide the user

🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

Fork the project
Create your feature branch (git checkout -b feature/AmazingFeature)
Commit your changes (git commit -m 'Add some AmazingFeature')
Push to the branch (git push origin feature/AmazingFeature)
Open a Pull Request

📝 License
This project is licensed under the MIT License - see the LICENSE file for details.
👏 Acknowledgements

Bootstrap - Front-end framework
Django - Web framework
Stripe - Payment processing
DM Mono & Bowlby One SC - Typography
Design inspiration from modern web aesthetics and sketchy UI trends


Developed with ❤️ by [Kim]
Get in touch: info@somechancer.com