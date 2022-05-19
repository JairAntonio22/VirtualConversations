const audio = document.querySelector('.tmp-player')
const record = document.querySelector('.record')

if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    let chunks = [];
    let recording = false;

    navigator.mediaDevices
        .getUserMedia({audio: true})
        .then((stream) => {
            const mediaRecorder = new MediaRecorder(stream)

            record.onclick = () => {
                if (recording) {
                    mediaRecorder.stop()
                    record.innerHTML = "Grabar"
                } else {
                    chunks = []
                    mediaRecorder.start()
                    record.innerHTML = "Detener"
                }

                recording = !recording
            }

            mediaRecorder.ondataavailable = (e) => {
                chunks.push(e.data)
            }

            mediaRecorder.onstop = (e) => {
                const blob = new Blob(chunks, {"type": "audio/ogg; codecs=opus"})
                const audioURL = window.URL.createObjectURL(blob)
                audio.src = audioURL
            }
        })
        .catch((err) => {
            console.log(err)
        })
} else {
    console.log("getUserMedia not supported on your browser!");
}
