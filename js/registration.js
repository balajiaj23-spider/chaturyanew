/**
 * College Technical Club Workshop Website — Registration Form Logic
 * Handles Form Validation, Query Param Auto-Selection, Confirmation Card Rendering,
 * LocalStorage Caching, and Django Backend API Integration Placeholder.
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
    } else if (courseParam.toLowerCase() === 'data-analytics') {
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
    className: document.getElementById('className').value,
    section: document.getElementById('section').value.trim(),
    hasLaptop: document.querySelector('input[name="hasLaptop"]:checked').value,
    timestamp: new Date().toISOString()
  };

  // Store registration object temporarily in LocalStorage
  saveRegistrationToLocalStorage(formData);

  // Send Data to Backend (Django API placeholder)
  sendDataToBackend(formData);

  // Render Confirmation Card UI
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

  // 2. ID Card Number
  const idCardNumber = document.getElementById('idCardNumber');
  if (!idCardNumber.value.trim()) {
    showFieldError(idCardNumber, 'College ID Card Number is required.');
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

  // 4. Phone Number (10-digit Indian Mobile Number)
  const phone = document.getElementById('phone');
  const phoneRegex = /^[6-9]\d{9}$/;
  if (!phoneRegex.test(phone.value.trim())) {
    showFieldError(phone, 'Please enter a valid 10-digit mobile number.');
    isValid = false;
  } else {
    clearFieldError(phone);
  }

  // 5. Stream
  const stream = document.getElementById('stream');
  if (!stream.value) {
    showFieldError(stream, 'Please select your academic stream.');
    isValid = false;
  } else {
    clearFieldError(stream);
  }

  // 6. Course
  const course = document.getElementById('course');
  if (!course.value) {
    showFieldError(course, 'Please select a workshop course.');
    isValid = false;
  } else {
    clearFieldError(course);
  }

  // 7. Class
  const className = document.getElementById('className');
  if (!className.value) {
    showFieldError(className, 'Please select your current year/class.');
    isValid = false;
  } else {
    clearFieldError(className);
  }

  // 8. Section
  const section = document.getElementById('section');
  if (!section.value.trim()) {
    showFieldError(section, 'Please specify your class section.');
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
    if (!input.value.trim()) {
      showFieldError(input, 'College ID Card Number is required.');
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
    const phoneRegex = /^[6-9]\d{9}$/;
    if (!phoneRegex.test(input.value.trim())) {
      showFieldError(input, 'Please enter a valid 10-digit mobile number.');
    } else {
      clearFieldError(input);
    }
  } else if (input.id === 'stream' || input.id === 'course' || input.id === 'className') {
    if (!input.value) {
      showFieldError(input, 'This field is required.');
    } else {
      clearFieldError(input);
    }
  } else if (input.id === 'section') {
    if (!input.value.trim()) {
      showFieldError(input, 'Section is required.');
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
  const formWrapper = document.querySelector('.form-wrapper');
  const successCard = document.getElementById('registrationSuccessCard');
  const detailsTable = document.getElementById('confirmationTableBody');

  if (formWrapper) formWrapper.style.display = 'none';
  if (successCard) successCard.classList.add('active');

  if (detailsTable) {
    detailsTable.innerHTML = `
      <tr><th>Registration ID</th><td><span class="badge">${data.id}</span></td></tr>
      <tr><th>Full Name</th><td>${escapeHtml(data.fullName)}</td></tr>
      <tr><th>College ID Card No.</th><td>${escapeHtml(data.idCardNumber)}</td></tr>
      <tr><th>Email Address</th><td>${escapeHtml(data.email)}</td></tr>
      <tr><th>Phone Number</th><td>+91 ${escapeHtml(data.phone)}</td></tr>
      <tr><th>Stream</th><td>${escapeHtml(data.stream)}</td></tr>
      <tr><th>Selected Workshop</th><td><strong style="color: var(--accent);">${escapeHtml(data.course)}</strong></td></tr>
      <tr><th>Class / Year</th><td>${escapeHtml(data.className)}</td></tr>
      <tr><th>Section</th><td>${escapeHtml(data.section)}</td></tr>
      <tr><th>Laptop Availability</th><td>${data.hasLaptop === 'Yes' ? '✓ Yes, Laptop Available' : '✕ No Laptop'}</td></tr>
    `;
  }

  // Scroll to top of section smooth
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

/**
 * DJANGO BACKEND INTEGRATION PLACEHOLDER
 * In a future Django implementation, replace or connect this function to a Django view API endpoint.
 * Example Django API endpoint: POST /api/register/
 */
function sendDataToBackend(registrationData) {
  /*
  fetch('/api/register/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken') // Django CSRF Token helper
    },
    body: JSON.stringify(registrationData)
  })
  .then(response => response.json())
  .then(data => console.log('Django Backend Response:', data))
  .catch(error => console.error('API Error:', error));
  */
  console.log('Registered successfully! Structured Object payload:', registrationData);
}
