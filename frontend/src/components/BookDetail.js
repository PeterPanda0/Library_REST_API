import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import axios from "axios";

function BookDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [book, setBook] = useState(null);

  useEffect(() => {
    axios
      .get(`https://programmer-library.run.place/api/books/${id}/`)
      .then(response => {
        setBook(response.data);
      })
      .catch(error => {
        console.error("Error fetching book details", error);
      });
  }, [id]);

  if (!book) {
    return <p>Загрузка...</p>;
  }

  return (
    <div>
      <h1>{book.title}</h1>
      <p>Количество: {book.count}</p>
      <p>Автор: {book.authors.map(author => author.name).join(", ")}</p>
      <p>Жанр: {book.genres.map(genre => genre.title).join(", ")}</p>
      <button
        onClick={() => navigate("/")}
        style={{
          backgroundColor: "black",
          color: "white",
          border: "none",
          padding: "10px 20px",
          cursor: "pointer",
          fontSize: "14px",
          borderRadius: "5px",
          marginTop: "10px"
        }}
      >
        Вернуться к списку
      </button>
    </div>
  );
}

export default BookDetail;
