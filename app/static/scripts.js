// --------------------------------------------
// === Toggle between light and dark themes ===
// --------------------------------------------
function toggleTheme() {
    // Get the current theme from the body tag
    const currentTheme = document.body.getAttribute("data-theme") || "light";

    // Determine the next theme
    const nextTheme = currentTheme === "light" ? "dark" : "light";

    // Apply the new theme to the body
    document.body.setAttribute("data-theme", nextTheme);

    // Update the toggle button text
    const buttonText = document.getElementById("toggleTheme");
    buttonText.innerText = nextTheme === "light" ? "Dark" : "Light";

    // --------------------------------------------------------------------------
    // === Inject current theme (?t=dark or ?t=light) into all internal links ===
    // --------------------------------------------------------------------------
    // Updates all internal links to include current theme as a GET parameter (e.g. /register?t=dark)
    function updateLinksWithThemeParam() {
        const links = document.querySelectorAll(
            'a[href^="/"], a[href^="#/"], a[href^="./"], a[href^="../"]'
        ); // Select all local <a> elements

        links.forEach((link) => {
            const url = new URL(link.href, window.location.origin); // Parse full URL from href
            url.searchParams.set("t", nextTheme); // Add or update the 't' query param
            link.href = url.pathname + url.search; // Write updated path and query back to href
        });
    }

    updateLinksWithThemeParam(); // Call the function to update links
}

// --------------------------------------------------------------------------------
// === Set the text inside the element with id "footerYear" to the current year ===
// --------------------------------------------------------------------------------
document.getElementById("footerYear").textContent = new Date().getFullYear();

document.addEventListener("DOMContentLoaded", () => {
    // ----------------------
    // === HTML Validator ===
    // ----------------------
    // Adapted from https://stackoverflow.com/a/10162353
    const html =
        "<!DOCTYPE " +
        document.doctype.name +
        (document.doctype.publicId
            ? ' PUBLIC "' + document.doctype.publicId + '"'
            : "") +
        (!document.doctype.publicId && document.doctype.systemId
            ? " SYSTEM"
            : "") +
        (document.doctype.systemId
            ? ' "' + document.doctype.systemId + '"'
            : "") +
        ">\n" +
        document.documentElement.outerHTML;
    document.querySelector(
        'form[action="https://validator.w3.org/check"] > input[name="fragment"]'
    ).value = html;
});
