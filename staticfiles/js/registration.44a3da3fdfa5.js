/**
 * College Technical Club Workshop Website — Registration Form Logic
 * Validates 9 registration fields, handles auto-selection from URL query params,
 * displays confirmation view without reloading, and saves data to localStorage.
 */

document.addEventListener('DOMContentLoaded', () => {
  const regForm = document.getElementById('workshopRegistrationForm');
  if (!regForm) return;

  // 1. Auto-select course from URL query parameter (e.g., registration.html?course=fullstack)
  autoSelectCourseFromUrl();

  // 2. Real-time blur validation for form input fields
  initRealtimeValidation(regForm);

  // 3. Form Submit Handler
  regForm.addEventListener('submit', handleFormSubmit);
});

/**
 * Parses URL query parameters to pre-fill the selected course
 */
function autoSelectCourseFromUrl() {
  const urlParams = new URLSearchParams(window.location.search);
  const courseParam = urlParams.get('course');
  const courseSelect = document.getElementById('course');

  if (courseParam && courseSelect) {
    if (courseParam.toLowerCase() === 'fullstack') {
      courseSelect.value = 'Full Stack Development';
    } else if (courseParam.toLowerCase() === 'data-analytics' || courseParam.toLowerCase() === 'dataanalytics') {
      courseSelect.value = 'Data Analytics';
    }
  }
}

/**
 * Form Submit Handler
 */
function handleFormSubmit(e) {
  e.preventDefault();

  const regForm = e.target;
  const isFormValid = validateAllFields(regForm);

  if (!isFormValid) {
    // Focus the first invalid field
    const firstInvalid = regForm.querySelector('.invalid');
    if (firstInvalid) firstInvalid.focus();
    return;
  }

  // Extract Form Data into a structured Object
  const formData = {
    id: 'REG-' + Date.now().toString().slice(-6),
    fullName: document.getElementById('fullName').value.trim(),
    idCardNumber: document.getElementById('idCardNumber').value.trim(),
    email: document.getElementById('email').value.trim(),
    phone: document.getElementById('phone').value.trim(),
    stream: document.getElementById('stream').value,
    course: document.getElementById('course').value,
    yearOfStudy: document.getElementById('className').value,
    section: document.getElementById('section').value,
    hasLaptop: document.querySelector('input[name="hasLaptop"]:checked').value,
    timestamp: new Date().toISOString()
  };

  // Store registration object temporarily in LocalStorage
  saveRegistrationToLocalStorage(formData);

  // Render Confirmation Card UI without full page reload
  renderConfirmationView(formData);
}

/**
 * Validates all 9 registration fields
 */
function validateAllFields(form) {
  let isValid = true;

  // 1. Full Name
  const fullName = document.getElementById('fullName');
  if (!fullName.value.trim() || fullName.value.trim().length < 2) {
    showFieldError(fullName, 'Please enter your full name (minimum 2 characters).');
    isValid = false;
  } else {
    clearFieldError(fullName);
  }

  // 2. College ID Number (e.g. 24CA000)
  const idCardNumber = document.getElementById('idCardNumber');
  const idRegex = /^[a-zA-Z0-9-]{3,15}$/;
  if (!idCardNumber.value.trim() || !idRegex.test(idCardNumber.value.trim())) {
    showFieldError(idCardNumber, 'Please enter a valid College ID Number (e.g. 24CA000).');
    isValid = false;
  } else {
    clearFieldError(idCardNumber);
  }

  // 3. Email Address
  const email = document.getElementById('email');
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email.value.trim())) {
    showFieldError(email, 'Please enter a valid email address.');
    isValid = false;
  } else {
    clearFieldError(email);
  }

  // 4. Phone Number (10-digit Mobile Number)
  const phone = document.getElementById('phone');
  const phoneRegex = /^[0-9]{10}$/;
  if (!phoneRegex.test(phone.value.trim())) {
    showFieldError(phone, 'Please enter a valid 10-digit phone number.');
    isValid = false;
  } else {
    clearFieldError(phone);
  }

  // 5. Stream
  const stream = document.getElementById('stream');
  if (!stream.value) {
    showFieldError(stream, 'Please select your stream.');
    isValid = false;
  } else {
    clearFieldError(stream);
  }

  // 6. Course
  const course = document.getElementById('course');
  if (!course.value) {
    showFieldError(course, 'Please select a course.');
    isValid = false;
  } else {
    clearFieldError(course);
  }

  // 7. Year of Study
  const yearOfStudy = document.getElementById('className');
  if (!yearOfStudy.value) {
    showFieldError(yearOfStudy, 'Please select your Year of Study.');
    isValid = false;
  } else {
    clearFieldError(yearOfStudy);
  }

  // 8. Section
  const section = document.getElementById('section');
  if (!section.value) {
    showFieldError(section, 'Please select your Section.');
    isValid = false;
  } else {
    clearFieldError(section);
  }

  // 9. Laptop Option
  const laptopChecked = document.querySelector('input[name="hasLaptop"]:checked');
  const laptopError = document.getElementById('laptopError');
  if (!laptopChecked) {
    if (laptopError) {
      laptopError.textContent = 'Please select whether you have a laptop.';
      laptopError.classList.add('active');
    }
    isValid = false;
  } else {
    if (laptopError) {
      laptopError.textContent = '';
      laptopError.classList.remove('active');
    }
  }

  return isValid;
}

/**
 * Displays error message for an input element
 */
function showFieldError(inputElement, message) {
  inputElement.classList.add('invalid');
  const errorContainer = document.getElementById(inputElement.id + 'Error');
  if (errorContainer) {
    errorContainer.textContent = message;
    errorContainer.classList.add('active');
  }
}

/**
 * Clears error state for an input element
 */
function clearFieldError(inputElement) {
  inputElement.classList.remove('invalid');
  const errorContainer = document.getElementById(inputElement.id + 'Error');
  if (errorContainer) {
    errorContainer.textContent = '';
    errorContainer.classList.remove('active');
  }
}

/**
 * Attach live validation on blur/input
 */
function initRealtimeValidation(form) {
  const inputs = form.querySelectorAll('.form-control');
  inputs.forEach(input => {
    input.addEventListener('blur', () => {
      validateSingleField(input);
    });
    input.addEventListener('input', () => {
      if (input.classList.contains('invalid')) {
        validateSingleField(input);
      }
    });
  });
}

function validateSingleField(input) {
  if (input.id === 'fullName') {
    if (!input.value.trim() || input.value.trim().length < 2) {
      showFieldError(input, 'Please enter your full name (minimum 2 characters).');
    } else {
      clearFieldError(input);
    }
  } else if (input.id === 'idCardNumber') {
    const idRegex = /^[a-zA-Z0-9-]{3,15}$/;
    if (!input.value.trim() || !idRegex.test(input.value.trim())) {
      showFieldError(input, 'Please enter a valid College ID Number (e.g. 24CA000).');
    } else {
      clearFieldError(input);
    }
  } else if (input.id === 'email') {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(input.value.trim())) {
      showFieldError(input, 'Please enter a valid email address.');
    } else {
      clearFieldError(input);
    }
  } else if (input.id === 'phone') {
    const phoneRegex = /^[0-9]{10}$/;
    if (!phoneRegex.test(input.value.trim())) {
      showFieldError(input, 'Please enter a valid 10-digit phone number.');
    } else {
      clearFieldError(input);
    }
  } else if (input.id === 'stream' || input.id === 'course' || input.id === 'className' || input.id === 'section') {
    if (!input.value) {
      showFieldError(input, 'This field is required.');
    } else {
      clearFieldError(input);
    }
  }
}

/**
 * Stores registration data in LocalStorage
 */
function saveRegistrationToLocalStorage(data) {
  try {
    const existing = JSON.parse(localStorage.getItem('workshop_registrations') || '[]');
    existing.push(data);
    localStorage.setItem('workshop_registrations', JSON.stringify(existing));
  } catch (err) {
    console.warn('LocalStorage unavailable:', err);
  }
}

/**
 * Renders Confirmation UI after successful submission
 */
function renderConfirmationView(data) {
  const formWrapper = document.getElementById('workshopRegistrationForm');
  const successCard = document.getElementById('registrationSuccessCard');
  const detailsTable = document.getElementById('confirmationTableBody');

  if (formWrapper) formWrapper.style.display = 'none';
  if (successCard) successCard.classList.add('active');

  if (detailsTable) {
    detailsTable.innerHTML = `
      <tr style="border-bottom: 1px solid var(--border-subtle);"><th style="padding: 0.75rem; text-align: left; color: var(--text-secondary);">Registration ID</th><td style="padding: 0.75rem; text-align: right;"><span class="badge" style="font-weight: 700;">${data.id}</span></td></tr>
      <tr style="border-bottom: 1px solid var(--border-subtle);"><th style="padding: 0.75rem; text-align: left; color: var(--text-secondary);">Full Name</th><td style="padding: 0.75rem; text-align: right; font-weight: 600; color: var(--text-primary);">${escapeHtml(data.fullName)}</td></tr>
      <tr style="border-bottom: 1px solid var(--border-subtle);"><th style="padding: 0.75rem; text-align: left; color: var(--text-secondary);">College ID Number</th><td style="padding: 0.75rem; text-align: right; font-weight: 600; color: var(--text-primary);">${escapeHtml(data.idCardNumber)}</td></tr>
      <tr style="border-bottom: 1px solid var(--border-subtle);"><th style="padding: 0.75rem; text-align: left; color: var(--text-secondary);">Email Address</th><td style="padding: 0.75rem; text-align: right; color: var(--text-primary);">${escapeHtml(data.email)}</td></tr>
      <tr style="border-bottom: 1px solid var(--border-subtle);"><th style="padding: 0.75rem; text-align: left; color: var(--text-secondary);">Phone Number</th><td style="padding: 0.75rem; text-align: right; color: var(--text-primary);">${escapeHtml(data.phone)}</td></tr>
      <tr style="border-bottom: 1px solid var(--border-subtle);"><th style="padding: 0.75rem; text-align: left; color: var(--text-secondary);">Stream</th><td style="padding: 0.75rem; text-align: right; color: var(--text-primary);">${escapeHtml(data.stream)}</td></tr>
      <tr style="border-bottom: 1px solid var(--border-subtle);"><th style="padding: 0.75rem; text-align: left; color: var(--text-secondary);">Course</th><td style="padding: 0.75rem; text-align: right; font-weight: 700; color: var(--accent);">${escapeHtml(data.course)}</td></tr>
      <tr style="border-bottom: 1px solid var(--border-subtle);"><th style="padding: 0.75rem; text-align: left; color: var(--text-secondary);">Year of Study</th><td style="padding: 0.75rem; text-align: right; color: var(--text-primary);">${escapeHtml(data.yearOfStudy)}</td></tr>
      <tr style="border-bottom: 1px solid var(--border-subtle);"><th style="padding: 0.75rem; text-align: left; color: var(--text-secondary);">Section</th><td style="padding: 0.75rem; text-align: right; color: var(--text-primary);">${escapeHtml(data.section)}</td></tr>
      <tr><th style="padding: 0.75rem; text-align: left; color: var(--text-secondary);">Laptop Availability</th><td style="padding: 0.75rem; text-align: right; font-weight: 600; color: ${data.hasLaptop === 'Yes' ? 'var(--accent)' : '#ff5f56'};">${data.hasLaptop === 'Yes' ? '✓ Yes (Laptop Available)' : '✕ No Laptop'}</td></tr>
    `;
  }

  // Scroll to top of form smooth
  window.scrollTo({ top: 100, behavior: 'smooth' });
}

/**
 * Helper to escape HTML characters
 */
function escapeHtml(str) {
  return str.replace(/[&<>"']/g, function(m) {
    return {
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      '"': '&quot;',
      "'": '&#039;'
    }[m];
  });
}
