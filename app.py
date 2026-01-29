"""
BLOOD – Blood Bank Application
A Flask-based blood bank management system for local development.
Milestone 1 – Local Development

EXTENDED WITH:
- Blood Compatibility AI Engine: Rule-based expert system for blood type compatibility
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import uuid
from blood_ai_engine import (
    get_compatible_donors,
    is_donor_compatible,
    filter_compatible_donors,
    get_compatibility_explanation
)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'BLOOD_BANK_SECRET_KEY_2026'
app.config['DEBUG'] = True

# ============================
# IN-MEMORY DATA STORAGE
# ============================

users = {}
requests_list = []
donation_history = {}

# ============================
# HELPER FUNCTIONS
# ============================

def generate_donor_id():
    """Generate unique donor ID"""
    return f"DONOR_{uuid.uuid4().hex[:8].upper()}"

def generate_requestor_id():
    """Generate unique requestor ID"""
    return f"REQ_{uuid.uuid4().hex[:8].upper()}"

def generate_request_id():
    """Generate unique request ID"""
    return f"REQ_{uuid.uuid4().hex[:12].upper()}"

def is_logged_in():
    """Check if user is logged in"""
    return 'email' in session

def get_current_user():
    """Get current logged-in user data"""
    if is_logged_in():
        return users.get(session['email'])
    return None

def get_user_requests(email):
    """Get all requests created by a requestor"""
    return [r for r in requests_list if r['requestor_email'] == email]

def get_active_requests():
    """Get all active blood requests"""
    return [r for r in requests_list if r['status'] == 'Requested']

def get_donor_accepted_requests(donor_email):
    """Get all requests accepted by a donor"""
    return [r for r in requests_list if r['donor_email'] == donor_email and r['status'] == 'Confirmed']

# ============================
# AI ENGINE HELPER FUNCTIONS
# ============================

def get_all_donors():
    """
    Get all registered donors.
    
    Returns:
        list: List of donor user dictionaries
    """
    return [user for user in users.values() if user['role'] == 'donor']

def get_compatible_donors_for_request(blood_group):
    """
    AI Helper: Get all donors with blood groups compatible with requested blood group.
    
    Uses the Blood Compatibility AI Engine to filter donors based on
    medical blood transfusion compatibility rules.
    
    Args:
        blood_group (str): The blood group that needs blood (receiver)
    
    Returns:
        list: List of compatible donor user dictionaries
    """
    all_donors = get_all_donors()
    compatible_groups = get_compatible_donors(blood_group)
    return [donor for donor in all_donors if donor['blood_group'] in compatible_groups]

def get_compatible_active_requests(donor_blood_group):
    """
    AI Helper: Get active requests compatible with a donor's blood group.
    
    Uses the Blood Compatibility AI Engine to filter requests where
    the donor's blood group can donate to the requested blood group.
    
    Args:
        donor_blood_group (str): The blood group of the donor
    
    Returns:
        list: List of compatible active request dictionaries
    """
    active_reqs = get_active_requests()
    return [
        req for req in active_reqs
        if is_donor_compatible(donor_blood_group, req['blood_group'])
    ]

# ============================
# ROUTES
# ============================

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/register-type')
def register_type():
    """Choose registration type (Donor/Requestor)"""
    return render_template('register_type.html')

@app.route('/register/<user_type>', methods=['GET', 'POST'])
def register(user_type):
    """Register as Donor or Requestor"""
    if user_type not in ['donor', 'requestor']:
        flash('Invalid registration type!', 'danger')
        return redirect(url_for('register_type'))
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        blood_group = request.form.get('blood_group', '')
        
        # Validation
        if not name or not email or not password or not blood_group:
            flash('All fields are required!', 'warning')
            return render_template('register.html', user_type=user_type)
        
        if password != confirm_password:
            flash('Passwords do not match!', 'warning')
            return render_template('register.html', user_type=user_type)
        
        if email in users:
            flash('Email already registered!', 'danger')
            return render_template('register.html', user_type=user_type)
        
        # Create user
        user_id = generate_donor_id() if user_type == 'donor' else generate_requestor_id()
        
        users[email] = {
            'id': user_id,
            'name': name,
            'email': email,
            'password': generate_password_hash(password),
            'blood_group': blood_group,
            'role': user_type
        }
        
        # Initialize donation history for donors
        if user_type == 'donor':
            donation_history[email] = []
        
        flash(f'Registration successful! Please login.', 'success')
        return redirect(url_for('login_type'))
    
    return render_template('register.html', user_type=user_type)

@app.route('/login-type')
def login_type():
    """Choose login type (Donor/Requestor)"""
    return render_template('login_type.html')

@app.route('/login/<user_type>', methods=['GET', 'POST'])
def login(user_type):
    """Login as Donor or Requestor"""
    if user_type not in ['donor', 'requestor']:
        flash('Invalid login type!', 'danger')
        return redirect(url_for('login_type'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        
        if not email or not password:
            flash('Email and password required!', 'warning')
            return render_template('login.html', user_type=user_type)
        
        user = users.get(email)
        
        if not user or not check_password_hash(user['password'], password):
            flash('Invalid email or password!', 'danger')
            return render_template('login.html', user_type=user_type)
        
        if user['role'] != user_type:
            flash(f'This account is registered as {user["role"].upper()}, not {user_type.upper()}!', 'danger')
            return render_template('login.html', user_type=user_type)
        
        # Set session
        session['email'] = email
        session['name'] = user['name']
        session['role'] = user['role']
        
        flash(f'Welcome, {user["name"]}!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('login.html', user_type=user_type)

@app.route('/dashboard')
def dashboard():
    """
    User dashboard (Donor or Requestor).
    
    AI INTEGRATION:
    - For requestors: Shows compatible donor count and AI compatibility information
    - For donors: Shows compatible requests count
    """
    if not is_logged_in():
        flash('Please login first!', 'danger')
        return redirect(url_for('login_type'))
    
    user = get_current_user()
    
    if user['role'] == 'requestor':
        user_requests = get_user_requests(session['email'])
        
        # AI ENGINE: For each request, get compatible donors
        requests_with_ai_info = []
        for req in user_requests:
            compatible_donors = get_compatible_donors_for_request(req['blood_group'])
            req_copy = req.copy()
            req_copy['compatible_donors_count'] = len(compatible_donors)
            req_copy['compatibility_explanation'] = get_compatibility_explanation(req['blood_group'])
            requests_with_ai_info.append(req_copy)
        
        return render_template('dashboard.html', 
                               user=user, 
                               user_requests=requests_with_ai_info,
                               role='requestor')
    else:  # donor
        accepted_requests = get_donor_accepted_requests(session['email'])
        donor_history = donation_history.get(session['email'], [])
        
        # AI ENGINE: Get compatible requests for this donor
        compatible_reqs = get_compatible_active_requests(user['blood_group'])
        
        return render_template('dashboard.html',
                               user=user,
                               accepted_requests=accepted_requests,
                               donation_history=donor_history,
                               compatible_requests_count=len(compatible_reqs),
                               all_active_requests_count=len(get_active_requests()),
                               role='donor')

@app.route('/request', methods=['GET', 'POST'])
def request_blood():
    """
    Create a blood request (Requestor only).
    
    AI INTEGRATION:
    - Displays AI compatibility information when creating a request
    - Shows compatible donor blood groups for the selected blood group
    """
    if not is_logged_in():
        flash('Please login first!', 'danger')
        return redirect(url_for('login_type'))
    
    user = get_current_user()
    if user['role'] != 'requestor':
        flash('Only requestors can create requests!', 'danger')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        blood_group = request.form.get('blood_group', '')
        units = request.form.get('units', '')
        
        if not blood_group or not units:
            flash('Blood group and units are required!', 'warning')
            return render_template('request.html', user=user)
        
        try:
            units = int(units)
            if units <= 0:
                flash('Units must be greater than 0!', 'warning')
                return render_template('request.html', user=user)
        except ValueError:
            flash('Units must be a valid number!', 'warning')
            return render_template('request.html', user=user)
        
        # Create request
        new_request = {
            'id': generate_request_id(),
            'blood_group': blood_group,
            'units': units,
            'requestor_email': session['email'],
            'donor_email': None,
            'status': 'Requested',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        requests_list.append(new_request)
        flash(f'Blood request created successfully! ID: {new_request["id"]}', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('request.html', user=user)

@app.route('/donors')
def donors():
    """
    View all active blood requests (Donor view).
    
    AI INTEGRATION:
    - Shows only blood requests that are compatible with the donor's blood group
    - Uses AI engine to filter requests based on blood compatibility rules
    - Displays AI compatibility information for each request
    """
    if not is_logged_in():
        flash('Please login first!', 'danger')
        return redirect(url_for('login_type'))
    
    user = get_current_user()
    if user['role'] != 'donor':
        flash('Only donors can view requests!', 'danger')
        return redirect(url_for('dashboard'))
    
    # AI ENGINE INTEGRATION: Get only AI-compatible active requests for this donor
    compatible_requests = get_compatible_active_requests(user['blood_group'])
    
    # AI ENGINE: Get all active requests for comparison (optional display)
    all_active_requests = get_active_requests()
    
    return render_template('donors.html', 
                         user=user, 
                         active_requests=compatible_requests,
                         all_active_requests=all_active_requests,
                         donor_blood_group=user['blood_group'])

@app.route('/donor/<donor_email>')
def donor_profile(donor_email):
    """View donor profile"""
    if donor_email not in users:
        flash('Donor not found!', 'danger')
        return redirect(url_for('index'))
    
    donor = users[donor_email]
    if donor['role'] != 'donor':
        flash('User is not a donor!', 'danger')
        return redirect(url_for('index'))
    
    donor_history_data = donation_history.get(donor_email, [])
    
    return render_template('donor_profile.html', 
                           donor=donor, 
                           donation_history=donor_history_data)

@app.route('/donate-blood/<request_id>', methods=['GET', 'POST'])
def donate_blood(request_id):
    """
    Accept a blood request (Donor accepts).
    
    AI INTEGRATION:
    - Verifies the donor's blood group is compatible before allowing acceptance
    - Uses AI engine to validate blood compatibility
    """
    if not is_logged_in():
        flash('Please login first!', 'danger')
        return redirect(url_for('login_type'))
    
    user = get_current_user()
    if user['role'] != 'donor':
        flash('Only donors can accept requests!', 'danger')
        return redirect(url_for('dashboard'))
    
    # Find the request
    blood_request = None
    for req in requests_list:
        if req['id'] == request_id:
            blood_request = req
            break
    
    if not blood_request:
        flash('Request not found!', 'danger')
        return redirect(url_for('donors'))
    
    if blood_request['status'] != 'Requested':
        flash('This request is no longer available!', 'danger')
        return redirect(url_for('donors'))
    
    # AI ENGINE: Check blood compatibility before allowing donation
    if not is_donor_compatible(user['blood_group'], blood_request['blood_group']):
        flash(f'Your blood group ({user["blood_group"]}) is not compatible with the requested blood group ({blood_request["blood_group"]})!', 'danger')
        return redirect(url_for('donors'))
    
    if request.method == 'POST':
        # Update request status to Confirmed
        blood_request['donor_email'] = session['email']
        blood_request['status'] = 'Confirmed'
        
        # Add to donation history
        donation_entry = {
            'request_id': blood_request['id'],
            'blood_group': blood_request['blood_group'],
            'requestor_email': blood_request['requestor_email'],
            'date_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        if session['email'] not in donation_history:
            donation_history[session['email']] = []
        
        donation_history[session['email']].append(donation_entry)
        
        flash(f'Blood request accepted! Request ID: {request_id}', 'success')
        return redirect(url_for('dashboard'))
    
    # Get compatibility explanation for display
    compatibility_info = get_compatibility_explanation(blood_request['blood_group'])
    
    return render_template('confirmation.html', 
                         blood_request=blood_request, 
                         user=user,
                         compatibility_info=compatibility_info)

@app.route('/confirm', methods=['GET', 'POST'])
def confirm():
    """Confirmation page for blood request acceptance"""
    if not is_logged_in():
        flash('Please login first!', 'danger')
        return redirect(url_for('login_type'))
    
    user = get_current_user()
    if user['role'] != 'donor':
        flash('Only donors can confirm requests!', 'danger')
        return redirect(url_for('dashboard'))
    
    return render_template('confirmation.html', user=user)

@app.route('/logout')
def logout():
    """Logout user"""
    if is_logged_in():
        user_name = session.get('name', 'User')
        session.clear()
        flash(f'Goodbye! You have been logged out.', 'info')
    return redirect(url_for('index'))

# ============================
# ERROR HANDLERS
# ============================

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors"""
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors"""
    flash('An internal error occurred!', 'danger')
    return redirect(url_for('index')), 500

# ============================
# RUN APPLICATION
# ============================

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
