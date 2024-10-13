import React, { useEffect, useState } from "react";
import axios from "axios";

function BookList() {
  const [books, setBooks] = useState([]);
  const [nextPage, setNextPage] = useState(null);
  const [previousPage, setPreviousPage] = useState(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [error, setError] = useState(null);
  const [file, setFile] = useState(null); // Для хранения выбранного файла

  const fetchBooks = (url = "http://localhost:8000/api/books/") => {
    axios
      .get(url)
      .then(response => {
        setBooks(response.data.results);
        setNextPage(response.data.next);
        setPreviousPage(response.data.previous);
      })
      .catch(error => {
        console.error("There was an error!", error);
        setError(error);
      });
  };

  useEffect(() => {
    fetchBooks();
  }, []);

  const handleSearch = () => {
    const url = `http://localhost:8000/api/books/?search=${searchQuery}`;
    fetchBooks(url);
  };

  const handleFileChange = (event) => {
    setFile(event.target.files[0]); // Сохраняем выбранный файл
  };

  const handleFileUpload = () => {
    if (!file) {
      alert("Пожалуйста, выберите файл для загрузки.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file); // Добавляем файл в FormData

    axios.post("http://localhost:8000/api/books/delivery/", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    })
    .then((response) => {
      alert("Файл успешно загружен!");
      fetchBooks(); // Обновляем список книг после загрузки
    })
    .catch((error) => {
      console.error("Ошибка при загрузке файла:", error);
      alert("Ошибка при загрузке файла.");
    });
  };

  return (
    <div>
      <h1 style={{ textAlign: "center", fontSize: "2em", marginBottom: "20px" }}>Список книг</h1>

      {/* Разметка для кнопок и строки поиска */}
      <div style={{ display: "flex", justifyContent: "center", alignItems: "center", marginBottom: "20px" }}>
        <input
          type="file"
          accept=".json"
          onChange={handleFileChange} // Добавляем обработчик выбора файла
          style={{ marginRight: "10px" }} // Отступ между кнопкой загрузки и строкой поиска
        />
        <button onClick={handleFileUpload}>Загрузить новые книги</button>

        <div style={{ margin: "0 20px" }}> {/* Отступы между элементами */}
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Поиск книг"
            style={{ marginRight: "10px" }} // Отступ между строкой поиска и кнопкой
          />
          <button onClick={handleSearch}>Поиск</button>
        </div>
      </div>

      {error && <p style={{ color: "red" }}>{error.message}</p>}
      <ul style={{ listStyleType: "none", padding: 0 }}>
        {books.map((book) => (
          <li key={book.id} style={{ padding: "10px" }}>
            <a href={`/book/${book.id}`} style={{ textDecoration: "none", color: "#000" }}>{book.title}</a>
          </li>
        ))}
      </ul>

      {/* Пагинация */}
      <div style={{ display: "flex", justifyContent: "center", marginTop: "20px" }}>
        {previousPage && (
          <button onClick={() => fetchBooks(previousPage)}>Предыдущая</button>
        )}
        {nextPage && (
          <button onClick={() => fetchBooks(nextPage)} style={{ marginLeft: "10px" }}>Следующая</button>
        )}
      </div>
    </div>
  );
}

export default BookList;
