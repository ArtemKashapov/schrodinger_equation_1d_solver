clearBtn = document.getElementById('clear-btn')
runBtn = document.getElementById('run-btn')


runBtn.addEventListener('click', run)
function run() {
    params = {
        'x_min': document.getElementById('x-min').value,
        'x_max': document.getElementById('x-max').value,
        'n_points': document.getElementById('n-points').value,
        'e_min': document.getElementById('e-min').value,
        'e_max': document.getElementById('e-max').value,
        'e_step': document.getElementById('e-step').value,
        'B': document.getElementById('const-b').value,
        'n_solutions': document.getElementById('n-solutions').value,
        'variant': document.getElementById('variant').value,
    }
    eel.run(params)
    console.log(params)
}

clearBtn.addEventListener('click', clear)

function clear() {
    document.getElementById('x-min').value = ''
    document.getElementById('x-max').value = ''
    document.getElementById('n-points').value = ''
    document.getElementById('e-min').value = ''
    document.getElementById('e-max').value = ''
    document.getElementById('e-step').value = ''
    document.getElementById('const-b').value = ''
    document.getElementById('n-solutions').value = ''
    document.getElementById('variant').value = ''
    setProgress("0")
}

eel.expose(setProgress)
function setProgress(progress) {
    let progressBar = document.getElementById('progress-bar')
    let progressVal = document.getElementById('progress-value')

    progressBar.setAttribute('style', "--i: " + progress + ";")
    progressVal.textContent = progress + "%"
}

eel.expose(show_message)
function show_message(message) {
    console.log(message==0)
    if (message==0) { 
        document.getElementById('msg-box').setAttribute('class', 'message error')
        document.getElementById('msg-text').textContent = 'No solutions found, try changing the parameters, perhaps reduce the search step dE'
        setTimeout(() => {
            document.getElementById('msg-box').setAttribute('class', 'message')
            document.getElementById('msg-text').textContent = ''
        }, 3000);
    } else if (message==-1) {
        document.getElementById('msg-box').setAttribute('class', 'message error')
        document.getElementById('msg-text').textContent = 'Invalid bounds for eigenvalues'
        setTimeout(() => {
            document.getElementById('msg-box').setAttribute('class', 'message')
            document.getElementById('msg-text').textContent = ''
        }, 3000);
    } else {
        document.getElementById('msg-box').setAttribute('class', 'message ok')
        if (message == 1) {
            endPart = ' solution.'
        } else {
            endPart = ' solutions.'
        }
        document.getElementById('msg-text').textContent = 'Equation solved, found ' + String(message) + endPart
        setTimeout(() => {
            document.getElementById('msg-box').setAttribute('class', 'message')
            document.getElementById('msg-text').textContent = ''
        }, 10000);
    }
}

document.addEventListener('contextmenu', event => event.preventDefault());


