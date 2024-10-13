import { render, screen } from '@testing-library/react';
import App from './App.js';

test('renders book list header', () => {
  render(<App />);
  const headerElement = screen.getByText(/Список книг/i);
  expect(headerElement).toBeInTheDocument();
});

test('renders upload button', () => {
  render(<App />);
  const uploadButton = screen.getByText(/Загрузить новые книги/i);
  expect(uploadButton).toBeInTheDocument();
});

test('renders search button', () => {
  render(<App />);
  const searchButton = screen.getByText(/Поиск/i);
  expect(searchButton).toBeInTheDocument();
});
