// popup.js
document.addEventListener('DOMContentLoaded', function() {
    chrome.storage.local.get('pastedText', function(data) {
      const pastedTextarea = document.getElementById('prompt-textarea');
      if (pastedTextarea) {
        pastedTextarea.value = data.pastedText || '';
      }
    });
  });
