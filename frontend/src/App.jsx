import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import CasosIA from "./pages/CasosIA";
import MassaDados from "./pages/MassaDados";
import MassaBancaria from "./pages/MassaBancaria";
import ExportarRelatorio from "./pages/ExportarRelatorio";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/casos" element={<CasosIA />} />
        <Route path="/massa" element={<MassaDados />} />
        <Route path="/bancaria" element={<MassaBancaria />} />
        <Route path="/exportar" element={<ExportarRelatorio />} />
      </Routes>
    </BrowserRouter>
  );
}
