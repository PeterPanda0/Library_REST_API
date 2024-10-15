import React, { useEffect, useState } from "react";
import axios from "axios";

function BookList() {
  const [books, setBooks] = useState([]);
  const [nextPage, setNextPage] = useState(null);
  const [previousPage, setPreviousPage] = useState(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [error, setError] = useState(null);
  const [file, setFile] = useState(null);

  const getApiUrl = (url) => {
    const protocol = window.location.protocol === "https:" ? "https://" : "http://";
    if (!url) {
      return `${protocol}programmer-library.run.place/api/books/`;
    }
    if (url.startsWith("http://") || url.startsWith("https://")) {
      return url.replace(/^http(s)?:\/\//, protocol);
    }
    return `${protocol}programmer-library.run.place${url}`;
  };
  const fetchBooks = (url = null) => {
    const apiUrl = getApiUrl(url);
    axios
      .get(apiUrl)
      .then((response) => {
        setBooks(response.data.results);
        setNextPage(response.data.next);
        setPreviousPage(response.data.previous);
      })
      .catch((error) => {
        console.error("There was an error!", error);
        setError(error);
      });
  };
  useEffect(() => {
    fetchBooks();
  }, []);

  const handleSearch = () => {
    const url = `https://programmer-library.run.place/api/books/?search=${searchQuery}`;
    fetchBooks(url);
  };

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleFileUpload = () => {
    if (!file) {
      alert("Пожалуйста, выберите файл для загрузки.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    axios
      .post("https://programmer-library.run.place/api/books/delivery/", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      })
      .then((response) => {
        alert("Файл успешно загружен!");
        fetchBooks();
      })
      .catch((error) => {
        console.error("Ошибка при загрузке файла:", error);
        alert("Ошибка при загрузке файла.");
      });
  };

  return (
    <div>
      <h1 style={{ textAlign: "center", fontSize: "2em", marginBottom: "20px" }}>Список книг</h1>

      <div style={{ display: "flex", justifyContent: "center", alignItems: "center", marginBottom: "20px" }}>
        <input
          type="file"
          accept=".json"
          onChange={handleFileChange}
          style={{ marginRight: "10px" }}
        />
        <button onClick={handleFileUpload}>Загрузить новые книги</button>

        <div style={{ margin: "0 20px" }}>
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Поиск книг"
            style={{ marginRight: "10px" }}
          />
          <button onClick={handleSearch}>Поиск</button>
        </div>
      </div>

      {error && <p style={{ color: "red" }}>{error.message}</p>}
      <ul style={{ listStyleType: "none", padding: 0 }}>
        {books.map((book) => (
          <li key={book.id} style={{ padding: "10px" }}>
            <a href={`/book/${book.id}`} style={{ textDecoration: "none", color: "#000" }}>
              {book.title}
            </a>
          </li>
        ))}
      </ul>

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
