// Strict mode is a directive introduced in ECMAScript 5 (ES5) that enforces stricter parsing and error handling in JavaScript.
// It helps catch common bugs and makes your code more secure and predictable.
//
// Benefits of strict mode:
// - Prevents use of undeclared variables
// - Disallows duplicate parameter names
// - Makes assignments to read-only properties throw errors
// - Eliminates silent errors
//
// Example:
// x = 10; // ❌ ReferenceError in strict mode (x is not declared)
"use strict";
// Everything below is in strict mode

/* -------------------------------------------- */
/* === Toggle between light and dark themes === */
/* -------------------------------------------- */
// Inject current theme (?t=dark or ?t=light) into all internal links
// Ref.: https://stackoverflow.com/a/11316355
function updateLinksFormsWithThemeParam(theme) {
    // Update all internal <a> links with theme param, without #
    const links = document.querySelectorAll(
        'a[href^="/"], a[href^="./"], a[href^="../"]'
    );
    links.forEach((link) => {
        const url = new URL(link.href, window.location.origin); // Parse full URL from href
        url.searchParams.set("t", theme); // Add or update the 't' query param
        link.href = url.pathname + url.search; // Write updated path and query back to href
    });

    // Update all <form> actions with theme param
    const forms = document.querySelectorAll("form[action]");
    forms.forEach((form) => {
        const url = new URL(form.action, window.location.origin); // Parse full URL from action
        url.searchParams.set("t", theme); // Add or update the 't' query param
        form.action = url.pathname + url.search; // Write updated path and query back to action
    });
}

// Button function to toggle the theme
// eslint-disable-next-line no-unused-vars
function toggleTheme() {
    // Get the current theme from the body tag
    const currentTheme = document.body.getAttribute("data-theme") || "light";

    // Determine the next theme
    const nextTheme = currentTheme === "light" ? "dark" : "light";

    // Apply the new theme to the body
    document.body.setAttribute("data-theme", nextTheme);

    // Update the toggle theme text
    // const themeText = document.getElementById("toggleTheme");
    // themeText.innerText = nextTheme === "light" ? "Dark" : "Light";

    // Call the function to update all links and forms
    updateLinksFormsWithThemeParam(nextTheme);

    // Update the URL to include ?t=... without reloading the page
    const newParams = new URLSearchParams(window.location.search);
    newParams.set("t", nextTheme);
    const newUrl =
        window.location.pathname +
        "?" +
        newParams.toString() +
        window.location.hash; // Preserve the hash if it exists
    // Update the URL in the address bar without reloading the page
    window.history.replaceState({}, "", newUrl);
}

/* -------------------------------------------------------------------------------- */
/* === Set the text inside the element with id "footerYear" to the current year === */
/* -------------------------------------------------------------------------------- */
document.getElementById("footerYear").textContent = new Date().getFullYear();

// ------------------------
// === DOMContentLoaded ===
// ------------------------
document.addEventListener("DOMContentLoaded", () => {
    /* === Update all links with theme param === */
    // Get the current theme from the body tag
    const currentTheme = document.body.getAttribute("data-theme");

    // Try reading from URL ?t=...
    const searchParams = new URLSearchParams(window.location.search);
    let urlTheme = searchParams.get("t") || currentTheme || "light"; // Default to light if not set

    // Call the function to update links and forms
    updateLinksFormsWithThemeParam(urlTheme);
});
