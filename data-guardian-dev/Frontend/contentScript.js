

if (window.location.href.startsWith('https://chat.openai.com')){
  document.addEventListener('paste', (event) => {
    event.preventDefault(); // New line: Prevent the default paste action.
    const pastedText = (event.clipboardData || window.clipboardData).getData('text');
    chrome.runtime.sendMessage({ action: 'pasteEvent', pastedText: pastedText });
    alert("You can't able to paste the data directly into Chat-GPT.\n Please use Guardian-AI extension to paste the data.");
});
}