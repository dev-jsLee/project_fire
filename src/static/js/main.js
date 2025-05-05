// API 기본 URL
const API_BASE_URL = 'http://localhost:8000/api/v1';

// 사용자 인증 관련 유틸리티
const auth = {
    // 로그인 처리
    login(userData) {
        // 세션 스토리지에 사용자 정보 저장
        sessionStorage.setItem('user', JSON.stringify(userData));
        this.updateHeader();
    },

    // 로그아웃 처리
    logout() {
        sessionStorage.removeItem('user');
        this.updateHeader();
        window.location.href = '/';
    },

    // 로그인 상태 확인
    isLoggedIn() {
        return !!sessionStorage.getItem('user');
    },

    // 현재 사용자 정보 가져오기
    getCurrentUser() {
        const userStr = sessionStorage.getItem('user');
        return userStr ? JSON.parse(userStr) : null;
    },

    // 헤더 메뉴 업데이트
    updateHeader() {
        const $headerNav = $('#common-header nav ul');
        if (!$headerNav.length) return;

        const isLoggedIn = this.isLoggedIn();
        const user = this.getCurrentUser();

        // 로그인/회원 정보 메뉴 아이템 찾기 또는 생성
        let $authMenuItem = $headerNav.find('.auth-menu-item');
        if (!$authMenuItem.length) {
            $authMenuItem = $('<li class="auth-menu-item"></li>').appendTo($headerNav);
        }

        if (isLoggedIn && user) {
            // 로그인 상태: 회원 정보 메뉴 표시
            $authMenuItem.html(`
                <div class="user-menu">
                    <span>${user.name || user.user_id}</span>
                    <div class="user-menu-dropdown">
                        <ul>
                            <li><a href="/mypage">마이페이지</a></li>
                            <li><a href="#" id="logout-btn">로그아웃</a></li>
                        </ul>
                    </div>
                </div>
            `);

            // 로그아웃 버튼에 이벤트 리스너 추가
            $('#logout-btn').on('click', (e) => {
                e.preventDefault();
                this.logout();
            });
        } else {
            // 비로그인 상태: 로그인/회원가입 링크 표시
            $authMenuItem.html(`
                <a href="/login">로그인</a>
            `);
        }
    }
};

// 게시글 목록 가져오기
async function getPosts() {
    try {
        const response = await $.get(`${API_BASE_URL}/posts`);
        return response;
    } catch (error) {
        console.error('Error fetching posts:', error);
        return [];
    }
}

// 게시글 목록 표시
function displayPosts(posts, category = '') {
    const $tbody = $('#post-list-body');
    if (!$tbody.length) return;
    
    // 기존 내용 지우기
    $tbody.empty();
    
    // 게시글 데이터로 행 추가
    posts.forEach(post => {
        // 카테고리 필터링
        if (category && post.category !== category) return;
        
        const date = new Date(post.created_at).toLocaleDateString();
        const $tr = $('<tr>').html(`
            <td>${post.id}</td>
            <td>${post.category || '일반'}</td>
            <td><a href="/posts/${post.id}">${post.title}</a></td>
            <td>${post.author}</td>
            <td>${date}</td>
            <td>${post.view_count}</td>
        `);
        $tbody.append($tr);
    });
}

// 페이지 로드 시 실행
$(document).ready(function() {
    // 헤더 상태 업데이트
    auth.updateHeader();

    // 게시글 목록 페이지인 경우
    const $postListBody = $('#post-list-body');
    if ($postListBody.length) {
        getPosts().then(posts => {
            displayPosts(posts);
            
            // 카테고리 필터 이벤트 처리
            $('#category').on('change', function() {
                const selectedCategory = $(this).val();
                displayPosts(posts, selectedCategory);
            });
        });
    }
    
    // 로그인 폼 처리
    $('#login-form').on('submit', async function(e) {
        e.preventDefault();
        
        const userId = $('#user_id').val();
        const password = $('#password').val();
        
        try {
            const response = await fetch('/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({
                    user_id: userId,
                    password: password
                })
            });

            if (response.ok) {
                const data = await response.json();
                auth.login(data);
                window.location.href = '/';
            } else {
                alert('로그인에 실패했습니다. 아이디와 비밀번호를 확인해주세요.');
            }
        } catch (error) {
            console.error('로그인 오류:', error);
            alert('로그인 처리 중 오류가 발생했습니다.');
        }
    });

    // 회원가입 폼 처리
    $('#register-form').on('submit', async function(e) {
        e.preventDefault();
        
        const formData = {
            user_id: $('#user_id').val(),
            password: $('#password').val(),
            password_confirm: $('#password_confirm').val(),
            email: $('#email').val(),
            nickname: $('#nickname').val()
        };

        // 비밀번호 확인
        if (formData.password !== formData.password_confirm) {
            alert('비밀번호가 일치하지 않습니다.');
            return;
        }

        try {
            await $.ajax({
                url: `${API_BASE_URL}/users/register`,
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(formData)
            });

            alert('회원가입이 완료되었습니다.');
            window.location.href = '/login';
        } catch (error) {
            console.error('회원가입 오류:', error);
            alert('회원가입에 실패했습니다. 다시 시도해주세요.');
        }
    });
});

// Header fragment 로드
fetch('/static/fragments/header.html')
    .then(response => response.text())
    .then(data => {
        const headerElement = document.getElementById('common-header');
        if (headerElement) {
            headerElement.outerHTML = data;
            // fragment 로드 후 헤더 상태 업데이트
            auth.updateHeader();
        }
    })
    .catch(error => console.error('Header fragment 로드 실패:', error));

// Footer fragment 로드
fetch('/static/fragments/footer.html')
    .then(response => response.text())
    .then(data => {
        const footerElement = document.querySelector('footer');
        if (footerElement) {
            footerElement.outerHTML = data;
        }
    })
    .catch(error => console.error('Footer fragment 로드 실패:', error));
