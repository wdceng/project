// HTML Validator
document.addEventListener('DOMContentLoaded', function () {
  // Adapted from https://stackoverflow.com/a/10162353
  const html =
    '<!DOCTYPE ' +
    document.doctype.name +
    (document.doctype.publicId
      ? ' PUBLIC "' + document.doctype.publicId + '"'
      : '') +
    (!document.doctype.publicId && document.doctype.systemId ? ' SYSTEM' : '') +
    (document.doctype.systemId ? ' "' + document.doctype.systemId + '"' : '') +
    '>\n' +
    document.documentElement.outerHTML;
  document.querySelector(
    'form[action="https://validator.w3.org/check"] > input[name="fragment"]'
  ).value = html;
});

// Toggle between light and dark themes
function toggleTheme() {
  // Get the current theme from the body tag
  const currentTheme = document.body.getAttribute('data-theme');

  // Determine the next theme
  const nextTheme = currentTheme === 'light' ? 'dark' : 'light';

  // Apply the new theme to the body
  document.body.setAttribute('data-theme', nextTheme);

  // Update the toggle button text
  const buttonText = document.getElementById('toggleTheme');
  buttonText.innerText = nextTheme === 'light' ? 'Dark' : 'Light';
}

// Set the text inside the element with id "footerYear" to the current year
document.getElementById('footerYear').textContent = new Date().getFullYear();
