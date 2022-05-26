const record = document.querySelector('.record')
const audio = document.querySelector('.tmp-player')

let blob = null
let audioURL = null

if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    let chunks = [];
    let recording = false;

    navigator.mediaDevices
        .getUserMedia({audio: true})
        .then((stream) => {
            const mediaRecorder = new MediaRecorder(stream)
            console.log(mediaRecorder.mimeType)

            record.onclick = () => {
                if (recording) {
                    mediaRecorder.stop()
                    record.innerHTML = "Grabar"
                } else {
                    mediaRecorder.start()
                    record.innerHTML = "Detener"
                }

                recording = !recording
            }

            mediaRecorder.ondataavailable = (e) => {
                chunks.push(e.data)
            }

            mediaRecorder.onstop = (e) => {
                blob = new Blob(chunks)
                audioURL = window.URL.createObjectURL(blob)
                audio.src = audioURL
                chunks = []
            }
        })
        .catch((err) => {
            console.log(err)
        })
} else {
    console.log("getUserMedia not supported on your browser!");
}

const sender = document.querySelector('.sender')

sender.onclick = () => {
    if (blob) {
        const formData = new FormData()
        formData.append('audio', blob, 'recording.ogg')

        fetch('/audio', {
            method: 'POST',
            body: formData
        }).then((response) => {
            console.log(response.url)
            window.location.replace(response.url);
        })
    }
}
