document.addEventListener("DOMContentLoaded", function () {

    // functions to open and close the popups
    window.openDeleteAccountPopup = function () {
        document.querySelector(".delete-popup").style.display = "flex";
    };

    window.closeDeleteAccountPopup = function () {
        document.querySelector(".delete-popup").style.display = "none";
    };

    window.openChangePasswordPopup = function () {
        document.querySelector(".change-password-popup").style.display = "flex";
    };

    window.closeChangePasswordPopup = function () {
        document.querySelector(".change-password-popup").style.display = "none";
    };
    // closes the popup when clicking outside of the content area
    const deletepopup = document.querySelector(".delete-popup");
     deletepopup.addEventListener("click", function (event) {
        window.closeDeleteAccountPopup();
    });
    // closes the popup when clicking outside of the content area
    const changepasswordpopup = document.querySelector(".change-password-popup");

        changepasswordpopup.addEventListener("click", function (event) {
        if (event.target === changepasswordpopup) {
            window.closeChangePasswordPopup();
        }
    });
});