// jest.setup.js
import "@testing-library/jest-dom";
window.HTMLElement.prototype.scrollIntoView = function () {};
