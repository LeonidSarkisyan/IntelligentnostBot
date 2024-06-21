const URL_CHAPTERS = window.location.href.split("/")
const RESULT_ID = URL_CHAPTERS[URL_CHAPTERS.length - 3]
const PASS_ID = URL_CHAPTERS[URL_CHAPTERS.length - 1]

console.log(RESULT_ID, PASS_ID)

// document.oncontextmenu = function() {
//     return false;
// };
//
// window.addEventListener('keydown', function(event) {
//     blockKey(event);
// });
//
// document.addEventListener('keydown', function(event) {
//     blockKey(event);
// });
//
// function blockKey(event) {
//     event.preventDefault()
// }


Spruce.store("data", {
    emptyQuestions: null,
    questions: [],
    minutes: 0,

    isPass: false,
    isComplete: false,
    currentQuestionIndex: 0,

    showModal: false,

    error: "",

    result: {}
})


Spruce.store("methods", {
    ToggleZoom(questionID) {
        const img = document.getElementById(`output_${questionID}`)

        img.classList.toggle("q_image_large")
    },

    ChooseGroup(aIndex, event) {
        const questions = JSON.parse(localStorage.getItem("questions"))

        questions[$store.data.currentQuestionIndex].data.answers[aIndex].group_index = Number(event.target.value)

        localStorage.setItem("questions", JSON.stringify(questions))
    },

    ChangeIndex(index){
        let newIndex = $store.data.currentQuestionIndex + index

        if (newIndex === $store.data.questions.length || newIndex < 0) {
            return
        }

        $store.data.currentQuestionIndex = newIndex
    },

    SaveAnswer(event, index, aIndex) {
        const questions = JSON.parse(localStorage.getItem("questions"))

        console.log(event)

        if (questions[index].type === "radio") {
            for (let j = 0; j < questions[index].answers.length; j++) {
                questions[index].answers[j].is_correct = false
            }
            questions[index].answers[aIndex].is_correct = event.srcElement.checked
        } else {
            questions[index].answers[aIndex].is_correct = event.srcElement.checked
        }

        localStorage.setItem("questions", JSON.stringify(questions))
    },

    ShowModal() {
        $store.data.showModal = true
    },

    CloseModal() {
      $store.data.showModal = false
    },

    CanCompleteTest() {
        const questions = JSON.parse(localStorage.getItem("questions"))
        let need = []

        let index = 0
        for (let q of questions) {
            switch (q.type) {
                case "group":
                    for (let a of q.data.answers) {
                        if (a.group_index === 0) {
                            need.push(index + 1)
                            break
                        }
                    }
                    break
                default:
                    let completeQ = false

                    for (let a of q.answers) {
                        if (a.is_correct === true) {
                            completeQ = true
                        }
                    }

                    if (!completeQ) {
                        need.push(index + 1)
                    }
            }
            index++
        }

        return [need.length <= 0, need]
    },

    async completeTest() {
        const questions = JSON.parse(localStorage.getItem("questions"))

        const timeText = document.getElementById("timer").innerText

        let timeParts = timeText.split(':');

        let hours = parseInt(timeParts[0]);
        let minutes = parseInt(timeParts[1]);
        let seconds = parseInt(timeParts[2]);

        let totalSeconds = (hours * 3600) + (minutes * 60) + seconds;

        try {
            const response = await axios.post(`/passing/${RESULT_ID}/solving/${PASS_ID}/results`, {
                questions: questions,
                time_pass: startTotalSeconds - totalSeconds
            })

            $store.data.result = response.data.result
            $store.data.isPass = false
            $store.data.showModal = false
            $store.data.isComplete = true
            socket.close(1000)
        } catch (e) {
            $store.data.error = e.response.data
        }
    }
})

const startButton = document.getElementById("startButton")

startButton.onclick = async () => {
    let response
    try {
        response = await axios.get(`/passing/${RESULT_ID}/solving/${PASS_ID}/questions`)
    } catch (e) {
        alert(e.response.data)
    }

    console.log(response.data)

    let questions = response.data.questions
    for (let i = 0; i < response.data.questions.length; i++) {
        if (questions[i].data === null) {
            questions[i].data = {
                groups: [],
                ranges: []
            }
        }
    }

    $store.data.questions = questions
    totalSeconds = response.data.access.passage_time * 60
    startTotalSeconds = totalSeconds
    document.getElementById('timer').innerText = TimeProcess(totalSeconds)
    localStorage.setItem("questions", JSON.stringify(questions))
    $store.data.isPass = true
    connectWebSocket()
    console.log(response.data)
}

let totalSeconds;
let startTotalSeconds;

let modal = document.getElementById("myModal");

window.onmousedown = function(event) {
    if (event.target === modal) {
        $store.data.showModal = false
        $store.data.error = ""
    }
}

window.addEventListener('beforeunload', function (e) {
    if (needProtect) {
        e.preventDefault();
        e.returnValue = 'Вы уверены, что хотите покинуть эту страницу? Вы не сможете вернуться к тесту.';
    }
});

let needProtect = true

let socket;

let tryCount = 45

function connectWebSocket() {
    if (window.location.hostname === "localhost") {
        socket = new WebSocket(`ws://${window.location.hostname}/passing/${RESULT_ID}/ws/student/${PASS_ID}`);
    } else {
        socket = new WebSocket(`wss://фаст-тест.рф/passing/${RESULT_ID}/ws/student/${PASS_ID}`);
    }

    socket.onopen = function(event) {
        console.log('WebSocket connected');
        socket.send('Hello, server!');
    };

    socket.onclose = function(event) {
        if (tryCount !== 0) {
            console.log('WebSocket disconnected');
            if (!$store.data.isPass) {
                setTimeout(connectWebSocket, 5000);
            }
        }
    };

    socket.onerror = function(error) {

        if (tryCount !== 0) {
            console.error('WebSocket error:', error);
            // Попытка переподключения через 5 секунд
            if (!$store.data.isPass) {
                setTimeout(connectWebSocket, 5000);
            }
            tryCount--
        }
    };

    socket.onmessage = async function(event) {
        const newResult = JSON.parse(event.data);
        console.log('Message received:', newResult);

        console.log(`total seconds = ${totalSeconds}`);
        console.log(`time_pass = ${newResult.time_pass}`);

        console.log(`total seconds - time_pass = ${totalSeconds - newResult.time_pass}`);

        if (totalSeconds - newResult.time_pass < 0) {
            await $store.methods.completeTest();
        }

        if (newResult.mark === -1) {
            document.getElementById("timer").innerText = TimeProcess(totalSeconds - newResult.time_pass);
        } else if (newResult.mark === -2) {
            needProtect = false;

            for (let i = 0; i < 100; i++) {
                window.location.href = "/passing/abort";
            }
        }

        console.log('Message received:', newResult);
    };
}


function TimeProcess(seconds) {
    let hours = Math.floor(seconds / 3600);
    let minutes = Math.floor((seconds % 3600) / 60);
    let remainingSeconds = seconds % 60;

    hours = pad(hours)
    minutes = pad(minutes)
    remainingSeconds = pad(remainingSeconds)

    return hours + ':' + minutes + ':' + remainingSeconds;
}

function pad(val) {
    return val > 9 ? val : '0' + val;
}
