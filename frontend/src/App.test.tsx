import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';

test('renders chat app title', () => {
  render(<App />);
  // Use getByRole to target the heading element
  const headerElement = screen.getByRole('heading', { name: /chat app/i });
  expect(headerElement).toBeInTheDocument();
});