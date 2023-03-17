
let pc = null;

class FarPiCamera extends FarPiElement {
    setup() {
        this.soucre = this.getAttribute("source");
        this.classList.add("w-full", "h-full");
        this.innerHTML =
            `<div id="media" class="w-full h-full">
                <video id="video" autoplay muted class="rounded-lg w-full h-full"></video>
            </div>`
        this.start();
        console.log('FarPiCamera added to page - ' + this.source);
    }

    negotiate() {
        pc.addTransceiver('video', {direction: 'recvonly'});
        // pc.addTransceiver('audio', {direction: 'recvonly'});
        return pc.createOffer().then(function (offer) {
            return pc.setLocalDescription(offer);
        }).then(function () {
            // wait for ICE gathering to complete
            return new Promise(function (resolve) {
                if (pc.iceGatheringState === 'complete') {
                    resolve();
                } else {
                    function checkState() {
                        if (pc.iceGatheringState === 'complete') {
                            pc.removeEventListener('icegatheringstatechange', checkState);
                            resolve();
                        }
                    }
                    pc.addEventListener('icegatheringstatechange', checkState);
                }
            });
        }).then(function () {
            let offer = pc.localDescription;
            return fetch(`http://192.168.0.44:8080/offer`, {  // TODO: Need to fix this static URL!!!
                body: JSON.stringify({
                    sdp: offer.sdp,
                    type: offer.type,
                }),
                headers: {
                    'Content-Type': 'application/json'
                },
                method: 'POST'
            });
        }).then(function (response) {
            return response.json();
        }).then(function (answer) {
            return pc.setRemoteDescription(answer);
        }).catch(function (e) {
            alert(e);
        });
    }

    start() {
        let config = {
            sdpSemantics: 'unified-plan'
        };

        pc = new RTCPeerConnection(config);

        // connect audio / video
        pc.addEventListener('track', function (evt) {
            if (evt.track.kind == 'video') {
                document.getElementById('video').srcObject = evt.streams[0];
            } else {
                document.getElementById('audio').srcObject = evt.streams[0];
            }
        });

        this.negotiate();
    }

    stop() {
        document.getElementById('stop').style.display = 'none';

        // close peer connection
        setTimeout(function () {
            pc.close();
        }, 500);
    }
}

customElements.define('farpi-camera', FarPiCamera);
