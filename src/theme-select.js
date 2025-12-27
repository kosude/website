/*
 * Copyright (c) 2025 Jack Bennett.
 * All Rights Reserved.
 *
 * See the LICENCE file for more information.
 */

const selectorEl = document.querySelector("aside#sidebar nav#theme-selector");

const themeAttributeName = "data-user-theme"; // name of theme attribute on HTML element
const themeStorageItemName = "userTheme"; // name under which selected theme is kept in local storage

// Make the theme selector visible in the sidebar
// This is done now so that it doesn't appear if JS is disabled
selectorEl.style.display = "";

// Function to switch page theme
function selectTheme(theme) {
    document.documentElement.setAttribute(themeAttributeName, theme);
}

// If a colour theme preference was previously stored, select the corresponding option in the theme selector (unless it is already selected)
function restoreThemePreference() {
    const theme = localStorage.getItem(themeStorageItemName);

    if (!theme) {
        // There is no stored preference to restore
        return;
    }

    const selectorOptionEl = selectorEl.querySelector(`#select-${theme}`);
    console.log(selectorOptionEl);

    if (!selectorOptionEl) {
        // The stored preference has no corresponding option in the selector - invalid
        localStorage.removeItem(themeStorageItemName);
        return;
    }

    if (document.documentElement.getAttribute(themeAttributeName) == theme) {
        // The stored preference's corresponding menu option is already selected
        return;
    }

    selectTheme(theme);
}

// Store an event target's value in localStorage
function storeThemePreference({ target }) {
    const theme = target.id.split("-")[1];
    localStorage.setItem(themeStorageItemName, theme);
}

if (selectorEl) {
    restoreThemePreference();

    // When the user changes their color scheme preference via the UI, store the new preference.
    selectorEl.querySelectorAll("li").forEach((x) => x.addEventListener("click", storeThemePreference));
}
