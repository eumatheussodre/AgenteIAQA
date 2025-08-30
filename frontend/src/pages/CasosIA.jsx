import React, { useState } from "react";
import api from "../api";
import { darkTheme } from "../darkTheme";

export default function CasosIA() {
  const [requisito, setRequisito] = useState("");
  const [arquivo, setArquivo] = useState(null);
  const [caso, setCaso] = useState("");
  const [loading, setLoading] = useState(false);
  const [erro, setErro] = useState("");

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file && (file.type === "application/pdf" || file.name.endsWith('.doc') || file.name.endsWith('.docx'))) {
      setArquivo(file);
      setErro("");
    } else {
      setErro("Apenas arquivos PDF, DOC ou DOCX são aceitos.");
      e.target.value = "";
    }
  };

  const gerarCaso = async (e) => {
    e.preventDefault();
    
    if (!requisito && !arquivo) {
      setErro("Informe um requisito ou faça upload de um arquivo.");
      return;
    }

    setLoading(true);
    setErro("");
    setCaso("");
    
    try {
      const formData = new FormData();
      
      if (arquivo) {
        formData.append('arquivo', arquivo);
      }
      
      if (requisito) {
        formData.append('requisito', requisito);
      }

      const resp = await api.post("/api/gerar-caso-ia", formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        }
      });
      
      if (resp.data && resp.data.caso) {
        setCaso(resp.data.caso);
      } else {
        setErro("Resposta inválida do backend.");
      }
    } catch (err) {
      setErro("Erro ao gerar caso de teste.");
    } finally {
      setLoading(false);
    }
  };

  const exportarParaExcel = async () => {
    try {
      const response = await api.post("/api/exportar-casos-excel", { 
        casos: caso 
      }, {
        responseType: 'blob'
      });
      
      // Criar link para download
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `casos_de_teste_${new Date().toISOString().split('T')[0]}.xlsx`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
      
    } catch (error) {
      setErro("Erro ao exportar para Excel");
    }
  };

  return (
    <div style={darkTheme.pageBg}>
      <div style={darkTheme.cardStyle}>
        <h2 style={darkTheme.titleStyle}>🧪 Gerar Caso de Teste (IA)</h2>
        <form onSubmit={gerarCaso}>
          <label style={darkTheme.labelStyle}>
            Requisito (Texto):
            <textarea
              value={requisito}
              onChange={e => setRequisito(e.target.value)}
              rows={4}
              style={darkTheme.inputStyle}
              placeholder="Digite o requisito ou deixe vazio para usar apenas o arquivo..."
            />
          </label>
          
          <div style={{ marginTop: '16px' }}>
            <label style={darkTheme.labelStyle}>
              ou Upload de Arquivo (.doc/.docx/.pdf):
              <input
                type="file"
                accept=".doc,.docx,.pdf"
                onChange={handleFileChange}
                style={{
                  ...darkTheme.inputStyle,
                  padding: '12px',
                  cursor: 'pointer'
                }}
              />
            </label>
            {arquivo && (
              <p style={{ color: '#4CAF50', marginTop: '8px', fontSize: '14px' }}>
                ✅ Arquivo selecionado: {arquivo.name}
              </p>
            )}
          </div>
          
          <button type="submit" disabled={loading} style={darkTheme.buttonStyle}>
            {loading ? "Gerando..." : "Gerar Caso de Teste"}
          </button>
        </form>
        {erro && <div style={darkTheme.erroStyle}>{erro}</div>}
        {caso && (
          <div style={{ marginTop: 24 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
              <strong style={{ fontSize: '18px', color: '#fff' }}>Casos de Teste Gerados:</strong>
              <button
                onClick={() => exportarParaExcel()}
                style={{
                  ...darkTheme.buttonStyle,
                  backgroundColor: '#4CAF50',
                  padding: '8px 16px',
                  fontSize: '14px'
                }}
              >
                📊 Exportar para Excel
              </button>
            </div>
            <div style={{
              backgroundColor: '#2d2d30',
              border: '1px solid #404040',
              borderRadius: '8px',
              padding: '24px',
              fontFamily: 'Consolas, monospace',
              fontSize: '14px',
              lineHeight: '1.8',
              color: '#e1e1e1',
              whiteSpace: 'pre-wrap',
              wordWrap: 'break-word',
              maxHeight: '600px',
              overflowY: 'auto',
              boxShadow: '0 4px 8px rgba(0,0,0,0.3)'
            }}>
              {caso}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

// ...estilos agora via darkTheme...
