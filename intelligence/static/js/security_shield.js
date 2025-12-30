/**
 * Security Shield - Client Side Protection
 * Disables right-click, keyboard shortcuts for source viewing, and developer tools.
 * Part of the Sovereign Intelligence Platform security layer.
 */
(function() {
    'use strict';

    // Disable Right Click
    document.addEventListener('contextmenu', function(e) {
        e.preventDefault();
        return false;
    });

    // Disable Keyboard Shortcuts
    document.addEventListener('keydown', function(e) {
        // Prevent F12
        if (e.key === 'F12' || e.keyCode === 123) {
            e.preventDefault();
            return false;
        }

        // Ctrl+Shift+I (DevTools)
        if (e.ctrlKey && e.shiftKey && (e.key === 'I' || e.key === 'i' || e.keyCode === 73)) {
            e.preventDefault();
            return false;
        }

        // Ctrl+Shift+J (DevTools Console)
        if (e.ctrlKey && e.shiftKey && (e.key === 'J' || e.key === 'j' || e.keyCode === 74)) {
            e.preventDefault();
            return false;
        }

        // Ctrl+Shift+C (Inspect Element)
        if (e.ctrlKey && e.shiftKey && (e.key === 'C' || e.key === 'c' || e.keyCode === 67)) {
            e.preventDefault();
            return false;
        }

        // Ctrl+U (View Source)
        if (e.ctrlKey && (e.key === 'U' || e.key === 'u' || e.keyCode === 85)) {
            e.preventDefault();
            return false;
        }
        
        // Ctrl+S (Save Page) - Optional but recommended for sovereignty
        if (e.ctrlKey && (e.key === 'S' || e.key === 's' || e.keyCode === 83)) {
            e.preventDefault();
            return false;
        }
    });

    // Console warning for anyone who manages to open it
    console.log("%c⚠️ Security Warning", "color: red; font-size: 30px; font-weight: bold;");
    console.log("%cThis is a sovereign intelligence system. Access to source code is restricted and monitored.", "font-size: 16px;");

})();
