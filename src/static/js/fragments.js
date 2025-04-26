/**
 * HTML fragment를 로드하고 지정된 요소에 삽입하는 함수
 * @param {string} fragmentPath - fragment 파일의 경로
 * @param {string} targetId - fragment를 삽입할 요소의 ID
 * @param {Function} postProcessCallback - fragment 로드 후 실행할 콜백 함수
 */
function loadFragment(fragmentPath, targetId, postProcessCallback) {
    $.get(fragmentPath)
        .done(function(html) {
            $(`#${targetId}`).html(html);
            
            // 후처리 콜백이 있으면 실행
            if (postProcessCallback) {
                postProcessCallback();
            }
        })
        .fail(function(jqXHR, textStatus, errorThrown) {
            console.error('Fragment 로드 중 오류 발생:', textStatus, errorThrown);
        });
}

// 페이지 로드 시 모든 fragment를 로드
$(document).ready(function() {
    // 헤더 fragment 로드
    if ($('#header-container').length) {
        loadFragment('/static/fragments/header.html', 'header-container', function() {
            // 헤더 로드 후 auth 상태 업데이트 (main.js의 auth 객체 사용)
            if (typeof auth !== 'undefined' && auth.updateHeader) {
                auth.updateHeader();
            }
        });
    }
    
    // 푸터 fragment 로드
    if ($('#footer-container').length) {
        loadFragment('/static/fragments/footer.html', 'footer-container');
    }
});

/**
 * 헤더의 링크 경로를 현재 페이지 위치에 맞게 조정
 * @param {boolean} isInPagesDirectory
 */
function adjustHeaderLinks(isInPagesDirectory) {
    const headerLinks = document.querySelectorAll('#header-container a');
    const prefix = isInPagesDirectory ? '../' : '';
    
    headerLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href && !href.startsWith('http') && !href.startsWith('#')) {
            link.setAttribute('href', prefix + href);
        }
    });
} 