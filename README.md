# 🎟️ Some Chancer – Modern Raffle Platform

> *"Not all who wander are lost. Some are just trying to win a PlayStation."*

Welcome to **Some Chancer**, a sleek, cheeky raffle platform where hand-drawn charm meets modern web wizardry. Users can buy tickets for exciting prize draws in style – squiggles, sketchy borders, and all.

⚠️ **Live Demo**: [somechancer.com](https://somechancer.com) – *Coming Soon!*

---

## ✨ Features

- 🎨 **Bold, Distinctive Design** – Eye-catching UI with animated elements, sketchy borders, and playful interactions.
- 🎰 **Dynamic Raffle System** – Create and manage raffles with flexible ticket options.
- 🔐 **Secure Payment Processing** – Stripe-powered for safe and seamless transactions.
- 👤 **User Accounts** – Personal dashboards to track tickets, winnings, and life choices.
- 🎲 **Transparent Winner Selection** – Fair, verifiable, and definitely not rigged.
- 📱 **Responsive Layout** – Works beautifully on mobile, tablet, and desktop.
- ⏱️ **Real-time Updates** – Live ticket counters and countdowns to crank up the suspense.
- 📬 **Email Notifications** – Automated updates for purchases, wins, and humblebrags.

---

## 🖼️ Screenshots

![Screenshot 1](https://your-image-url.com)
![Screenshot 2](https://your-image-url.com)
![Screenshot 3](https://your-image-url.com)
![Screenshot 4](https://your-image-url.com)

---

## 🛠️ Tech Stack

| Layer         | Technology                 |
|---------------|----------------------------|
| Backend       | Django 5.2, Python 3.12     |
| Frontend      | HTML5, CSS3, JavaScript     |
| Styling       | Bootstrap 5, Custom CSS     |
| Database      | PostgreSQL                 |
| Payments      | Stripe API                 |
| Caching       | Redis                      |
| Task Queue    | Django-Q                   |
| Deployment    | Docker, Nginx, Gunicorn    |

---

## 🚀 Getting Started

### 📦 Prerequisites

- Python 3.10+
- PostgreSQL
- Redis
- Stripe account

### ⚙️ Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/some-chancer.git
cd some-chancer

# Set up virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy and configure environment variables
cp .env.example .env
# Edit .env with your Stripe keys and database config

# Run migrations
python manage.py migrate

# Create an admin user
python manage.py createsuperuser

# Start the development server
python manage.py runserver
```
Visit http://127.0.0.1:8000/ in your browser and marvel at your creation.

## 🌟 Usage

### 🔧 Admin Panel

- Visit [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
- Log in using your superuser credentials
- Create and manage raffles, view transactions, and more

---

### 🎟️ Creating a Raffle

1. Go to **Raffles → Add Raffle**
2. Fill in:
   - Title & Description
   - Upload a beautiful image (*or a cursed one – your vibe, your choice*)
   - Set ticket price & quantity
   - Start and end dates
   - Toggle **Featured** to promote it on the homepage
3. Click **Save** – boom, you're in business.

---

### 🏆 Drawing a Winner

Once a raffle ends:

- Log in as an admin
- Go to the raffle’s detail page
- Click **Draw Winner**
- The system will fairly (and magically) pick someone
- An email is sent to the lucky human

---

## 💡 Design Inspiration

Some Chancer’s look is inspired by:

- ✏️ **Sketchy Aesthetics** – SVG filters simulate a hand-drawn style
- 🧠 **Fluid Typography** – Text that adapts like a shape-shifting cat
- 💫 **Animated Effects** – Subtle motion to guide and delight
- 🎨 **Custom Buttons** – Playful styles with interactive feedback
- 🌈 **Bold Colors** – High-impact palette for high-stakes raffles

---

## 🤝 Contributing

We love code. We love pull requests more.

```bash
# Fork the project
git checkout -b feature/AmazingFeature

# Do your thing
git commit -m 'Add some AmazingFeature'
git push origin feature/AmazingFeature

# Submit a PR 
# (Preferably with no bugs 🐛)
```
## 📝 License

This project is licensed under the **MIT License**.  
See the [LICENSE](LICENSE) file for details.

---

## 👏 Acknowledgements

- **Django** – Backend framework of dreams  
- **Bootstrap** – Clean, responsive styling  
- **Stripe** – Making payments easy and secure  
- **Fonts** – *DM Mono* & *Bowlby One SC* – stylin’ and profilin’  
- **Inspiration** – From sketchy UIs (in style, not in trustworthiness)

---

## Developed With <3

Built by **Kim** with 💻 + ☕ + maybe a few 🍕.  

📬 Get in touch: [info@somechancer.com](mailto:info@somechancer.com)  
🐙 GitHub: [github.com/kimatron/some-chancer](https://github.com/kimatron/some-chancer)
