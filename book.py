import streamlit as st
import requests
import google.generativeai as genai

# [TODO]API 설정
GOOGLE_BOOKS_API_KEY = "AIzaSyDnA8NjMFQdWogCK0swY5DHagMUJeCuaOE"

# Gemini API 키 가져오기(키 가져오는 방식에 따라 이 부분 수정필요합니다.)
#with open("private") as f:
 #   api_key = f.read().strip()
api_key="AIzaSyBA47UPEA6lfKAQXJc1-Qnq90ERt4PI1sU"
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# Streamlit 앱 제목
st.title("AI 기반 책 추천 및 리뷰 생성기")

# 책 검색 함수 (Google Books API 사용)
def search_books(query):
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}&key={GOOGLE_BOOKS_API_KEY}"
    # [TODO] url로 요청을 하여 결과를 받음.
    response = requests.get(url)
    return response.json().get("items", [])

# [TODO] 검색할 책 제목을 사용자가 입력하도록 합니다(st)
query =st.text_input("검색할 책 제목을 입력하세요.")

# 책 검색 버튼(st)
if st.button("책 검색") and query:
    books = search_books(query)
    if books:
        # 첫 번째 책 정보
        book = books[0]  # 검색 결과 중 첫 번째 책 선택
        volume_info = book["volumeInfo"]
        title = volume_info.get("title", "제목 없음")
        authors = ", ".join(volume_info.get("authors", "저자 정보 없음"))
        description = volume_info.get("description", "설명 없음")
        publisher = volume_info.get("publisher", "출판사 정보 없음")
        page_count = volume_info.get("pageCount", "페이지 수 정보 없음")
        
        # [TODO] 첫 번째 책 정보를 출력하기(st)
        st.subheader(f"**제목**: {title}")
        st.write(f"**저자**: {authors}")
        st.write(f"**출판사**: {publisher}")
        st.write(f"**페이지 수**: {page_count}")
        st.write(f"**설명**: {description}")
        
        # [TODO]AI 기반 리뷰 생성
        prompt = f"{authors} 작가가 쓴'{title}'에 대한 리뷰를 간결하게 한국어로 작성해줘."
        # 해당 프롬프트를 모델에 전달한 결과를 받는다
        response = model.generate_content(prompt)
        
        # [TODO] AI 생성 리뷰 텍스트만 추출하여 출력
        st.subheader("**AI 생성 리뷰**")
        st.write(response.text)
    else:
        st.write("검색 결과가 없습니다.")
