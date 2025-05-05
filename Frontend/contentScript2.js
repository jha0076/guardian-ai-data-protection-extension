  
if (window.location.href.startsWith('https://chat.openai.com')){
    let textAreaElement = document.getElementById('prompt-textarea');
    chrome.storage.local.get('protectedText', function(data) {

            textAreaElement.value = data.protectedText || '';
    
      });
}
