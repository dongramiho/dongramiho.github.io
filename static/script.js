function fetchMovieRecommendations() {
    const movieName = document.getElementById('movieName').value;
    // 폼 데이터를 서버로 전송하는 POST 요청을 발송
    fetch('/results', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `movie_title=${encodeURIComponent(movieName)}`
    })
    .then(response => response.json())
    .then(data => {
        // 서버로부터 받은 데이터로 결과 표시 영역 업데이트
        if (data.error) {
            document.getElementById('displayArea').innerHTML = `<p>${data.error}</p>`;
        } else {
            let content = `<h2>${data.movie_title}</h2><ul>`;
            data.recommendations.forEach(movie => {
                content += `<li>${movie.title} <img src="${movie.poster_path}" alt="${movie.title} Poster"></li>`;
            });
            content += `</ul>`;
            document.getElementById('displayArea').innerHTML = content;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('displayArea').innerHTML = '<p>에러가 발생했습니다.</p>';
    });
}


function resetPage() {
    document.getElementById('movieName').value = ''; // 입력 필드 비우기
    document.getElementById('displayArea').innerHTML = ''; // 결과 표시 영역 비우기
    return false; // 링크의 기본 동작을 방지
}

function openModal() {
    document.getElementById("myModal").style.display = "block";
}

function closeModal() {
    document.getElementById("myModal").style.display = "none";
}

// 모달 외부 클릭 시 닫기
window.onclick = function (event) {
    if (event.target == document.getElementById("myModal")) {
        closeModal();
    }
};

// 닫기 버튼 클릭 시 모달 닫기 연결
document.getElementsByClassName("close")[0].onclick = function () {
    closeModal();
};
