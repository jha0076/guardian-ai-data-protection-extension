const inputFileElement = document.getElementById('fileInput');
const inputTextElement = document.getElementById('prompt-textarea');
const outputTextElement = document.getElementById('output-text');
const anonymizeTextBtn = document.getElementById('AnonymizeTextBtn');
const redactTextBtn = document.getElementById('RedactTextBtn');
const reviewTextBtn = document.getElementById('ReviewTextBtn');
const anonymizeFileBtn = document.getElementById('AnonymizeFileBtn');
const redactFileBtn = document.getElementById('RedactFileBtn');
const dataBtn = document.getElementById('dataButton');
const filesBtn = document.getElementById('filesButton');
const filesSection = document.getElementById('filesSection');
const fileUploadSection = document.getElementById("file-upload-section");
const fileDownloadSection = document.getElementById('file-download-section');
const presidioRadio = document.getElementById('pre-guard');
const bedrockRadio = document.getElementById('bedrock-guard');
const spinner = document.getElementById('spinner');
const spinnerFiles = document.getElementById('spinner-files');
const clipBoardBtn = document.getElementById('copy-to-clip-board-btn');
const copyBrowserBtn = document.getElementById('copy-to-browser-btn');
const outputTextArea = document.getElementById('otput-textarea');
const copyOrgText = document.getElementById('copy-org-text-btn');
const copyOrgTextBrowser = document.getElementById('copy-org-text-btn-browser');
const url = 'http://127.0.0.1:5000/'

let processFilesData = async function(file,fileName,path){
    spinnerFiles.classList.remove('d-none');
    if (fileName.endsWith('.txt')){


        let formData = new FormData()
        formData.append('file', file);

        let options = {
          method:'POST',
          body:formData
        }
        try{

          let fileNameType = path.includes('anonymize') ? 'anonymized_' : 'redacted_';
          let response = await fetch(url+path,options)

          let res = await response.json()
          let text = res['text']
          let blob = new Blob([text], { type: 'text/plain' });
          let a = document.createElement('a')
          a.href = window.URL.createObjectURL(blob);
          a.classList.add('file-link');
          a.download = fileNameType+fileName;
          fileDownloadSection.appendChild(a)
          a.textContent=fileNameType+fileName;
          
        }
        catch(error){
          alert('Something happend wrong! Please try again.')
          console.log(error)
        }

    }
    else if(fileName.endsWith('.csv')){
      let formData = new FormData()
        formData.append('file', file);

        let options = {
          method:'POST',
          body:formData
        }
        try{
          let fileNameType = path.includes('anonymize') ? 'anonymized_' : 'redacted_';
          let response = await fetch(url+path,options)
          let res = await response.text()
          let text = res
          console.log(text)
          let blob = new Blob([text], { type: 'text/csv' });
          let a = document.createElement('a')
          a.href = window.URL.createObjectURL(blob);
          a.classList.add('file-link');
          a.download = fileNameType+fileName;
          fileDownloadSection.appendChild(a)
          a.textContent= fileNameType+fileName;
        }
        catch(error){
          alert('Something happend wrong! Please try again.')
          console.log(error)
        }
    }
    else{
      alert('Currently our tool supports .csv or .txt files only! Please upload .csv or .txt files to process')
    }
    spinnerFiles.classList.add('d-none')
    
}




const processTextData = async function (path,text){
    spinner.classList.remove('d-none');
    outputTextElement.innerHTML='';
    outputTextArea.value = '';
      let options = {
        method:'POST'
      }
      let req_url = url+path+'?text='+text
      console.log(url+path)
      let res_text
      try {
        const response = await fetch(req_url,options);
        const jsonData = await response.json();

        const obj = jsonData['mapping']
        const org_values = []
        const new_values = []
        for (let entity_type in obj){
            for (let entity in obj[entity_type]){
                if (org_values.indexOf(entity)===-1){
                    org_values.push(entity)
                }
                if (new_values.indexOf(obj[entity_type][entity])===-1){
                    new_values.push(obj[entity_type][entity])
                }
            }
        }
        res_text = jsonData['text']
        outputTextArea.value=res_text;
        if(path === 'anonymize_text'){
          for (let value of new_values){
            console.log(value)
            res_text = res_text.replaceAll(value,"<span class='pii-value'>"+value+"</span>")
          }
        }
        else if(path==='review_text'){
          for (let value of org_values){
            console.log(value)
            res_text = res_text.replaceAll(value,"<span class='pii-value'>"+value+"</span>")
          }
        }
        res_text = res_text.replaceAll('\n','</br>')
        
        outputTextElement.innerHTML=res_text

      } catch (error) {
        console.log(error);
        alert('Something happend wrong! Please try again.')
      }
      spinner.classList.add('d-none');


}


const changeGuardian = async function(guardian){
  let options = {
    method:'POST'
  }
  let req_url = url+'change_guardian?guardian='+guardian;
  try{
    const response = await fetch(req_url,options);
  }
  catch(error){
    console.log(error)
  }

}





// Function to set the active button
function setActiveButton(buttonId) {
    const buttons = document.querySelectorAll('.nav-link');
    buttons.forEach(button => {
      button.classList.remove('active');
    });
    const activeButton = document.getElementById(buttonId);
    activeButton.classList.add('active');
  }
  
  // Functionality for Data and Files buttons
 dataBtn.addEventListener("click", () => {
    // Your logic for the Data page
    console.log("Data Button Clicked!");
    setActiveButton("dataButton");
    document.getElementById("pageTitle").textContent = 'Protect your data with AI from AI';
    document.getElementById("dataSection").style.display = "block";
    document.getElementById("filesSection").style.display = "none";
  });
  
 filesBtn.addEventListener("click", () => {
    // Your logic for the Files page
    console.log("Files Button Clicked!");
    setActiveButton("filesButton");
    document.getElementById("pageTitle").textContent = 'Protect your files with AI from AI';
    document.getElementById("dataSection").style.display = "none";
    document.getElementById("filesSection").style.display = "block";
  });
  

  function getTextFromInput(){
      let text = inputTextElement.value;
      if (text === ''){
          alert("Please Enter Text Data To Process!")
      }
      else{
        return text
      }
  }

  // Button click functions for Data Page (Replace with your actual logic)
  anonymizeTextBtn.addEventListener("click", () => {
    console.log("Anonymize Button Clicked!");

    let text = encodeURIComponent(getTextFromInput())

    processTextData('anonymize_text',text)
  
  });
  
  redactTextBtn.addEventListener("click", () => {
    console.log("Redact Button Clicked!");

    let text = encodeURIComponent(getTextFromInput())
    processTextData('redact_text',text)

  });
  
  reviewTextBtn.addEventListener("click", () => {
    console.log("Identify Button Clicked!");
    let text = encodeURIComponent(getTextFromInput())
    processTextData('review_text',text)
  });


  // Button click functions for Data Page (Replace with your actual logic)
  anonymizeFileBtn.addEventListener("click", () => {
    console.log("Anonymize Button Clicked!");
    fileDownloadSection.innerHTML='';
    let file = inputFileElement.files[0]
    if (!file){
      alert('Please Upload A File To Process')
    }
    else{
      if (file.name.endsWith('.txt')){
        processFilesData(file,file.name,'anonymize_text_file')
      }
      else{
        processFilesData(file,file.name,'anonymize_csv')
      }
    }
  });
  
  redactFileBtn.addEventListener("click", () => {
    console.log("Redact Button Clicked!");
    fileDownloadSection.innerHTML='';
    let file = inputFileElement.files[0]
    if (!file){
      alert('Please Upload A File To Process')
    }
    else{
      if (file.name.endsWith('.txt')){
        processFilesData(file,file.name,'redact_text_file')
      }
      else{
        processFilesData(file,file.name,'redact_csv')
      } 
    }
  });
  


  presidioRadio.addEventListener('click',(e)=>{
    changeGuardian(e.target.value)
  })

  bedrockRadio.addEventListener('click',(e)=>{
    changeGuardian(e.target.value)
  })
 




  
  function copyToClipboard() {
    console.log("Copy to Clipboard");
    if (outputTextArea.value ===''){
      alert('Please add your input to process!')
    }
    else{
    
      navigator.clipboard.writeText(outputTextArea.value)
      alert('Modified Text Successfully Copied To Clipboard!')
    }
  }

  
  clipBoardBtn.addEventListener('click',copyToClipboard)



   
  function copyOrgToClipboard() {
    console.log("Copy to Clipboard");
    if (inputTextElement.value ===''){
      alert('Please add some text to process and copy!')
    }
    else{
    
      navigator.clipboard.writeText(inputTextElement.value)
      alert('Successfully Copied To Clipboard!')
    }
  }

  copyOrgText.addEventListener('click',copyOrgToClipboard)

  function copyToBrowser(){
    console.log("Copy to Clipboard");
    if (outputTextArea.value===''){
      alert('Please add some text to process and copy!')
    }
    else{
      alert('Modified text copied to browser.')
      const protectedText = outputTextArea.value;
      chrome.runtime.sendMessage({ action: 'pasteText', text: protectedText });
    }
  }

  copyBrowserBtn.addEventListener('click',copyToBrowser)
 
  function copyOrgToBrowser(){
    console.log("Copy to Clipboard");
    if (inputTextElement.value===''){
      alert('Please add some text to process and copy!')
    }
    else{
      alert('Text copied to browser.')
      const protectedText = inputTextElement.value;
      chrome.runtime.sendMessage({ action: 'pasteText', text: protectedText });
    }
  }
  copyOrgTextBrowser.addEventListener('click',copyOrgToBrowser)


// Check if we're on xyz.com and if the text box exists
if (window.location.host === 'chat.openai.com') {
  window.addEventListener('DOMContentLoaded', (event) => {
    const searchBox = document.getElementsByName('textarea')[0];
    console.log(searchBox)
    if (searchBox) {
      searchBox.addEventListener('focus', (e) => {
        injectPopup();
        searchBox.addEventListener('paste', (e) => {
          e.preventDefault(); // Prevent the default paste action
          // You can access the clipboard data using e.clipboardData if needed
          inputTextElement.value = e.clipboardData
        });
      });
    }
  });
}
console.log(chrome)
