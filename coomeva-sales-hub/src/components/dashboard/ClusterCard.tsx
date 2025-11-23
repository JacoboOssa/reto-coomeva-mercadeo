import { useState, useRef } from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Upload, CheckCircle2, XCircle, FileSpreadsheet } from "lucide-react";
import { LoadingSpinner } from "@/components/ui/loading-spinner";
import { Modal } from "@/components/ui/modal";
import { ProgressBar } from "@/components/ui/progress-bar";
import { useToast } from "@/hooks/use-toast";

const WEBHOOK_URL = "https://jacobossaguarnizoo19.app.n8n.cloud/webhook-test/e0d3199e-1b27-4ee7-8787-56f7e0ef680f";

export function ClusterCard() {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [showModal, setShowModal] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const { toast } = useToast();

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (!selectedFile) return;

    // Validate file type
    const validTypes = [
      "text/csv",
      "application/vnd.ms-excel",
      "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ];

    if (!validTypes.includes(selectedFile.type) && 
        !selectedFile.name.endsWith(".csv") && 
        !selectedFile.name.endsWith(".xlsx") && 
        !selectedFile.name.endsWith(".xls")) {
      toast({
        variant: "destructive",
        title: "Formato no válido",
        description: "Por favor, selecciona un archivo CSV o XLSX.",
      });
      return;
    }

    setFile(selectedFile);
  };

  const handleUpload = async () => {
    if (!file) {
      toast({
        variant: "destructive",
        title: "Archivo requerido",
        description: "Por favor, selecciona un archivo para subir.",
      });
      return;
    }

    setLoading(true);
    setProgress(0);
    setError(null);
    setSuccessMessage(null);

    // Simulate progress while uploading
    const progressInterval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 90) {
          clearInterval(progressInterval);
          return prev;
        }
        return prev + 10;
      });
    }, 300);

    try {
      // Crear FormData para enviar el archivo
      const formData = new FormData();
      formData.append("file", file); // El archivo con la key "file"
      formData.append("opcion", "2"); // Parámetros adicionales

      const response = await fetch(WEBHOOK_URL, {
        method: "POST",
        // NO incluir Content-Type header, el navegador lo establece automáticamente con boundary
        body: formData,
      });

      clearInterval(progressInterval);
      setProgress(100);

      if (!response.ok) {
        throw new Error(`Error ${response.status}: ${response.statusText}`);
      }

      // Procesar respuesta del webhook
      const data = await response.json();
      console.log("Respuesta de clusterización:", data);

      // Verificar si la respuesta indica error
      if (data && data.success === false) {
        // Error del agente (modelo o base de datos)
        throw new Error(data.message || "Ocurrió un error en el procesamiento.");
      }

      // Respuesta exitosa
      if (data && data.success === true) {
        setSuccessMessage(data.message || "Operación completada correctamente.");
      } else {
        throw new Error("Respuesta inesperada del servidor.");
      }

      setShowModal(true);
      setFile(null);
      if (fileInputRef.current) {
        fileInputRef.current.value = "";
      }
    } catch (err) {
      clearInterval(progressInterval);
      const errorMessage = err instanceof Error ? err.message : "Error desconocido";
      setError(errorMessage);
      setShowModal(true);
    } finally {
      setLoading(false);
      setTimeout(() => setProgress(0), 1000);
    }
  };

  const closeModal = () => {
    setShowModal(false);
    setSuccessMessage(null);
    setError(null);
  };

  return (
    <>
      <Card className="p-5 hover:shadow-lg transition-all bg-gradient-to-br from-card to-secondary/30">
        <div className="space-y-4">
          <div className="flex items-center gap-3">
            <div className="inline-flex items-center justify-center w-11 h-11 bg-accent/10 rounded-xl">
              <FileSpreadsheet className="w-6 h-6 text-accent" />
            </div>
            <div>
              <h2 className="text-xl font-bold text-foreground">Clusterizar Clientes</h2>
              <p className="text-xs text-muted-foreground">Sube archivo CSV o XLSX</p>
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="file-upload" className="text-sm font-medium">Archivo de clientes</Label>
            <div className="flex flex-col gap-2">
              <input
                ref={fileInputRef}
                id="file-upload"
                type="file"
                accept=".csv,.xlsx,.xls"
                onChange={handleFileChange}
                disabled={loading}
                className="hidden"
              />
              <Button
                type="button"
                variant="outline"
                onClick={() => fileInputRef.current?.click()}
                disabled={loading}
                className="w-full h-11 justify-start text-sm"
              >
                <Upload className="w-5 h-5 mr-2" />
                {file ? file.name : "Seleccionar archivo"}
              </Button>
              {file && (
                <p className="text-xs text-muted-foreground truncate">
                  <span className="font-medium text-foreground">{file.name}</span>
                </p>
              )}
            </div>
          </div>

          {loading && progress > 0 && (
            <ProgressBar progress={progress} />
          )}

          <Button 
            onClick={handleUpload}
            disabled={loading || !file}
            className="w-full h-11 text-sm font-medium"
            size="lg"
          >
            {loading ? (
              <>
                <LoadingSpinner size="sm" className="mr-2" />
                Subiendo...
              </>
            ) : (
              <>
                <Upload className="w-5 h-5 mr-2" />
                Subir y procesar
              </>
            )}
          </Button>
        </div>
      </Card>

      <Modal
        isOpen={showModal}
        onClose={closeModal}
        title={error ? "Error en el procesamiento" : "Procesamiento exitoso"}
        footer={
          <Button onClick={closeModal}>Cerrar</Button>
        }
      >
        {error ? (
          <div className="flex flex-col items-center gap-4 py-6">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-destructive/10 rounded-full">
              <XCircle className="w-8 h-8 text-destructive" />
            </div>
            <div className="text-center space-y-3">
              <h3 className="text-lg font-semibold text-foreground">
                No se pudo completar el procesamiento
              </h3>
              <div className="bg-destructive/5 border border-destructive/20 rounded-lg p-4">
                <p className="text-sm text-foreground font-medium">{error}</p>
              </div>
              <p className="text-xs text-muted-foreground">
                Por favor, verifica el archivo e intenta nuevamente
              </p>
            </div>
          </div>
        ) : successMessage ? (
          <div className="flex flex-col items-center gap-4 py-6">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-primary/10 rounded-full">
              <CheckCircle2 className="w-8 h-8 text-primary" />
            </div>
            <div className="text-center space-y-3">
              <h3 className="text-lg font-semibold text-foreground">
                ¡Proceso completado!
              </h3>
              <div className="bg-primary/5 border border-primary/20 rounded-lg p-4">
                <p className="text-sm text-foreground font-medium">{successMessage}</p>
              </div>
              <p className="text-xs text-muted-foreground">
                Los clientes han sido clusterizados correctamente
              </p>
            </div>
          </div>
        ) : null}
      </Modal>
    </>
  );
}
