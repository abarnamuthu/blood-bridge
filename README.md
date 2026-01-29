# 🩸 BLOOD – Blood Bank Application

## Project Overview

**BLOOD** is a Flask-based blood bank management system designed for **Milestone 1 – Local Development**. It enables users to register as either **Donors** or **Requestors**, manage blood requests, and maintain donation history—all using in-memory data storage with Python dictionaries and lists.

### Tagline
*"Donate blood, save lives."*

---

## Features

### 👥 User Management
- **Dual-Role System**: Register and login as Donor or Requestor
- **Role-Based Access Control**: Different dashboards for each role
- **Session Management**: Secure Flask sessions for authentication
- **Password Security**: Werkzeug password hashing (bcrypt)

### 🩸 Donor Features
- View all active blood requests from the community
- Accept blood requests with confirmation workflow
- Maintain detailed donation history
- Track blood groups and requestor information
- View donor profiles with donation statistics

### 🏥 Requestor Features
- Create blood requests specifying blood group and units needed
- Monitor request status (Requested → Confirmed)
- Track which donors have accepted requests
- View all personal requests in dashboard

### 📊 Data Management
- **In-Memory Storage**: Uses Python dictionaries and lists (NO database)
- **Unique ID Generation**: UUID-based IDs for donors, requestors, and requests
- **Real-Time Updates**: Status changes reflected immediately across dashboards
- **Donation History**: Complete tracking of all donations with timestamps

### 🎨 User Interface
- Modern, responsive design with Jinja2 templates
- Bootstrap-inspired CSS styling
- Flash messages for all actions (success, error, warning, info)
- Mobile-friendly layout
- Blood group color-coded badges

---

## Project Structure

```
BLOODBANK/
│
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── README.md                       # This file
│
├── templates/
│   ├── index.html                 # Home page
│   ├── register_type.html         # Choose registration role
│   ├── register.html              # Registration form
│   ├── login_type.html            # Choose login role
│   ├── login.html                 # Login form
│   ├── dashboard.html             # User dashboard (role-specific)
│   ├── request.html               # Create blood request
│   ├── donors.html                # View available requests (donor view)
│   ├── donor_profile.html         # Donor profile and history
│   └── confirmation.html          # Confirm blood donation
│
└── static/
    └── css/
        └── style.css              # Main stylesheet
```

---

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Step 1: Navigate to Project Directory
```bash
cd "c:\Users\acer\OneDrive\Documents\BLOOD BRIDGE\BLOODBANK"
```

### Step 2: Create Virtual Environment (Recommended)
```bash
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

---

## How to Run

### Start the Application
```bash
python app.py
```

### Access the Application
Open your web browser and navigate to:
```
http://127.0.0.1:5000
```

### Debug Mode
The application runs in **debug mode** by default, allowing:
- Auto-reloading on code changes
- Detailed error messages
- Development console

---

## User Flow Explanation

### Donor Flow
1. **Register** → Choose "Donor" role and provide details (name, email, blood group, password)
2. **Login** → Access donor dashboard
3. **View Requests** → Browse all active blood requests
4. **Accept Request** → Click "Accept & Donate Blood"
5. **Confirm Donation** → Review details and confirm donation
6. **View History** → Track all donations in dashboard

### Requestor Flow
1. **Register** → Choose "Requestor" role and provide details
2. **Login** → Access requestor dashboard
3. **Create Request** → Specify blood group and units needed
4. **Monitor Status** → Track request status (Requested → Confirmed)
5. **View Acceptance** → See which donor accepted the request
6. **Dashboard** → View all personal requests

---

## Data Storage

### Users Dictionary
```python
users = {
  "email": {
    "id": "DONOR_xxxxx" or "REQ_xxxxx",
    "name": "User Name",
    "email": "user@example.com",
    "password": "hashed_password",
    "blood_group": "O+",
    "role": "donor" or "requestor"
  }
}
```

### Requests List
```python
requests = [
  {
    "id": "REQ_xxxxxxxxxxxxx",
    "blood_group": "O+",
    "units": 2,
    "requestor_email": "requestor@example.com",
    "donor_email": "donor@example.com" or None,
    "status": "Requested" or "Confirmed",
    "timestamp": "2026-01-23 10:30:45"
  }
]
```

### Donation History Dictionary
```python
donation_history = {
  "donor_email": [
    {
      "request_id": "REQ_xxxxxxxxxxxxx",
      "blood_group": "O+",
      "requestor_email": "requestor@example.com",
      "date_time": "2026-01-23 10:30:45"
    }
  ]
}
```

---

## API Routes

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Home page |
| `/register-type` | GET | Choose registration role |
| `/register/<user_type>` | GET, POST | Register as donor/requestor |
| `/login-type` | GET | Choose login role |
| `/login/<user_type>` | GET, POST | Login as donor/requestor |
| `/dashboard` | GET | User dashboard (role-specific) |
| `/request` | GET, POST | Create blood request |
| `/donate-blood/<request_id>` | GET, POST | Accept and donate blood |
| `/donors` | GET | View available requests |
| `/donor/<donor_email>` | GET | View donor profile & history |
| `/confirm` | GET, POST | Confirm donation |
| `/logout` | GET | Logout user |

---

## Key Features Implementation

### Session Authentication
- Uses Flask `session` object to store user email, name, and role
- Secure logout clears all session data
- Role-based access control on protected routes

### Password Security
- Werkzeug `generate_password_hash()` for storing passwords
- `check_password_hash()` for authentication
- Never stores plain text passwords

### UUID Generation
- **Donor ID**: `DONOR_<8-char-hex>`
- **Requestor ID**: `REQ_<8-char-hex>`
- **Request ID**: `REQ_<12-char-hex>`

### Status Lifecycle
```
Requested → (Donor Accepts) → Confirmed
```

---

## Testing the Application

### Test Scenario 1: Donor Registration & First Donation
1. Register as Donor with email: `john@example.com`, blood group: `O+`
2. Login as donor
3. View available requests
4. Accept a request
5. Verify donation in history

### Test Scenario 2: Requestor Creates Request
1. Register as Requestor with email: `hospital@example.com`
2. Login as requestor
3. Create blood request (O+, 2 units)
4. See request appear in donor view
5. After donor accepts, status shows "CONFIRMED"

### Test Data
```
Donor Email: donor1@test.com | Password: donor123 | Blood: O+
Requestor Email: req1@test.com | Password: req123 | Blood: AB+
```

---

## Future Enhancements (Milestone 2+)

### Cloud Integration
- **AWS EC2**: Deploy application to AWS cloud
- **AWS S3**: Store user documents and blood reports
- **AWS Lambda**: Serverless functions for notifications

### Database Implementation
- **Amazon DynamoDB**: Replace in-memory storage with NoSQL database
- **AWS RDS**: Optional relational database for complex queries
- **Data Persistence**: Survive application restarts

### Additional Features
- Email notifications for request acceptance
- Push notifications for urgent requests
- Appointment scheduling for donors
- Blood bank inventory management
- Blood expiry tracking
- Admin dashboard for blood bank staff
- Analytics and reporting
- Donor eligibility questionnaire
- Request priority levels
- Multi-location blood bank support

### DevOps & Deployment
- **Docker**: Containerize the application
- **boto3**: AWS SDK integration
- **CloudWatch**: Monitoring and logging
- **CI/CD Pipeline**: Automated testing and deployment
- **API Gateway**: REST API with authentication
- **Cognito**: User authentication service

---

## Technologies Used

### Backend
- **Flask 2.3.3**: Web framework
- **Werkzeug 2.3.7**: WSGI utilities and security

### Frontend
- **Jinja2**: Template engine
- **HTML5**: Markup language
- **CSS3**: Styling and responsive design
- **JavaScript**: Client-side interactions

### Python Libraries
- `uuid`: Generate unique identifiers
- `datetime`: Timestamp management
- `werkzeug.security`: Password hashing

---

## Configuration

### Flask Settings
```python
app.secret_key = 'BLOOD_BANK_SECRET_KEY_2026'
app.config['DEBUG'] = True
app.run(debug=True, host='127.0.0.1', port=5000)
```

### Port & Host
- **Host**: `127.0.0.1` (localhost)
- **Port**: `5000`
- **URL**: `http://127.0.0.1:5000`

---

## Code Structure

### MVC Pattern
- **Models**: User, Request, DonationHistory (in-memory data structures)
- **Views**: Jinja2 templates in `/templates`
- **Controllers**: Routes and logic in `app.py`

### Best Practices
- Clean, readable, and well-commented code
- Separated concerns (routing, authentication, data management)
- Consistent naming conventions
- Error handling with flash messages
- Input validation on all forms

---

## Troubleshooting

### Port Already in Use
```bash
# Change port in app.py
app.run(debug=True, host='127.0.0.1', port=5001)
```

### Module Not Found
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### Template Not Found
- Ensure templates are in the correct `/templates` directory
- Template names are case-sensitive

### Session Issues
- Clear browser cookies if session problems occur
- Restart the application
- Check browser's privacy settings

---

## Security Notes

⚠️ **Important**: This is a **Milestone 1 development version** for local testing only.

### Current Limitations
- Passwords stored with basic hashing (no salt configuration)
- No HTTPS/SSL in development
- Debug mode enabled (not for production)
- In-memory storage (data lost on restart)
- No CSRF protection
- Limited input validation

### Production Recommendations
- Disable debug mode
- Use HTTPS/SSL certificates
- Implement CSRF protection
- Add comprehensive input validation
- Use a proper database (DynamoDB, PostgreSQL)
- Implement rate limiting
- Add logging and monitoring
- Use environment variables for secrets
- Implement proper error handling

---

## License

This project is developed for educational purposes. All rights reserved.

---

## Author

BLOOD – Blood Bank Application Team  
**Version**: 1.0 (Milestone 1)  
**Release Date**: January 2026

---

## Support & Feedback

For issues, suggestions, or contributions, please refer to the application dashboard or contact the development team.

---

**"Donate blood, save lives."** 🩸
