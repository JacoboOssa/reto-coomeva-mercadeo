import { useState } from "react";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Search, XCircle } from "lucide-react";
import { Modal } from "@/components/ui/modal";
import { ProgressModal } from "./ProgressModal";
import { useToast } from "@/hooks/use-toast";

const WEBHOOK_URL = "https://jacobossaguarnizoo19.app.n8n.cloud/webhook-test/e0d3199e-1b27-4ee7-8787-56f7e0ef680f";

interface ClientProfileData {
  arquetipo_y_perfil: string;
  mensaje: string;
  idea: string;
  canal: string;
  recomendacion: string;
}

interface ConsultCardProps {
  onResultReady: (data: ClientProfileData) => void;
}

interface ProgressStep {
  label: string;
  completed: boolean;
}

export function ConsultCard({ onResultReady }: ConsultCardProps) {
  const [cedula, setCedula] = useState("");
  const [producto, setProducto] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showErrorModal, setShowErrorModal] = useState(false);
  const [progressSteps, setProgressSteps] = useState<ProgressStep[]>([]);
  const { toast } = useToast();

  const updateStep = (stepIndex: number) => {
    setProgressSteps((prev) =>
      prev.map((step, index) => ({
        ...step,
        completed: index <= stepIndex,
      }))
    );
  };

  const handleConsult = async () => {
    if (!cedula.trim() || !producto.trim()) {
      toast({
        variant: "destructive",
        title: "Campos requeridos",
        description: "Por favor, ingresa el número de cédula y el producto.",
      });
      return;
    }

    setLoading(true);
    setError(null);

    // Inicializar pasos de progreso
    setProgressSteps([
      { label: "Consultando cliente...", completed: false },
      { label: "Analizando perfil financiero...", completed: false },
      { label: "Generando arquetipo...", completed: false },
      { label: "Creando idea de valor...", completed: false },
      { label: "Definiendo estrategia de comunicación...", completed: false },
    ]);

    try {
      // Simular progreso mientras se hace la petición
      updateStep(0);
      
      await new Promise((resolve) => setTimeout(resolve, 800));
      updateStep(1);

      const response = await fetch(WEBHOOK_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          cedula: cedula.trim(),
          producto: producto.trim(),
          opcion: "1",
        }),
      });

      await new Promise((resolve) => setTimeout(resolve, 600));
      updateStep(2);

      if (!response.ok) {
        throw new Error(`Error ${response.status}: ${response.statusText}`);
      }

      await new Promise((resolve) => setTimeout(resolve, 600));
      updateStep(3);

      const data = await response.json();
      
      // Debug: ver qué llega exactamente
      console.log("Respuesta completa:", data);
      console.log("Es array?:", Array.isArray(data));
      console.log("Primer elemento:", data[0]);

      // Verificar si es una respuesta de error de n8n
      if (Array.isArray(data) && data.length > 0 && data[0].success === false) {
        throw new Error(data[0].message || "Ocurrió un error en el procesamiento");
      }
      if (data && data.success === false) {
        throw new Error(data.message || "Ocurrió un error en el procesamiento");
      }

      await new Promise((resolve) => setTimeout(resolve, 600));
      updateStep(4);

      // Extraer datos de la estructura de n8n: [{ output: { ... } }]
      let profileData: ClientProfileData | null = null;
      
      if (Array.isArray(data) && data.length > 0) {
        if (data[0].output) {
          // Formato n8n: [{ output: { arquetipo_y_perfil, mensaje, ... } }]
          profileData = data[0].output as ClientProfileData;
        } else if (data[0].arquetipo_y_perfil) {
          // Formato array directo: [{ arquetipo_y_perfil, mensaje, ... }]
          profileData = data[0] as ClientProfileData;
        }
      } else if (data && typeof data === "object") {
        if (data.output) {
          // Formato con output: { output: { ... } }
          profileData = data.output as ClientProfileData;
        } else if (data.arquetipo_y_perfil) {
          // Formato directo: { arquetipo_y_perfil, mensaje, ... }
          profileData = data as ClientProfileData;
        }
      }

      // Validar que tenga los campos requeridos
      if (!profileData) {
        console.error("No se pudo extraer profileData. Estructura recibida:", data);
        throw new Error("No se pudo procesar la estructura de la respuesta");
      }

      if (!profileData.arquetipo_y_perfil || !profileData.mensaje || !profileData.idea) {
        console.error("Faltan campos. ProfileData:", profileData);
        throw new Error("Faltan campos requeridos en la respuesta");
      }

      await new Promise((resolve) => setTimeout(resolve, 400));
      onResultReady(profileData);
      toast({
        title: "Consulta exitosa",
        description: "El perfil del cliente ha sido generado correctamente.",
      });
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "Error desconocido";
      setError(errorMessage);
      setShowErrorModal(true);
    } finally {
      setLoading(false);
      setProgressSteps([]);
    }
  };

  const closeErrorModal = () => {
    setShowErrorModal(false);
    setError(null);
  };

  return (
    <>
      <Card className="p-5 hover:shadow-lg transition-all bg-gradient-to-br from-card to-secondary/30">
        <div className="space-y-4">
          <div className="flex items-center gap-3">
            <div className="inline-flex items-center justify-center w-11 h-11 bg-primary/10 rounded-xl">
              <Search className="w-6 h-6 text-primary" />
            </div>
            <div>
              <h2 className="text-xl font-bold text-foreground">Consultar Cliente</h2>
              <p className="text-xs text-muted-foreground">
                Busca información por cédula
              </p>
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="cedula" className="text-sm font-medium">
              Número de cédula
            </Label>
            <Input
              id="cedula"
              type="text"
              placeholder="Ej: 1234567890"
              value={cedula}
              onChange={(e) => setCedula(e.target.value)}
              disabled={loading}
              className="h-11 text-base"
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="producto" className="text-sm font-medium">
              Producto
            </Label>
            <Input
              id="producto"
              type="text"
              placeholder="Ej: Crédito hipotecario"
              value={producto}
              onChange={(e) => setProducto(e.target.value)}
              disabled={loading}
              className="h-11 text-base"
              onKeyDown={(e) => e.key === "Enter" && handleConsult()}
            />
          </div>

          <Button
            onClick={handleConsult}
            disabled={loading}
            className="w-full h-11 text-sm font-medium"
            size="lg"
          >
            <Search className="w-5 h-5 mr-2" />
            Consultar
          </Button>
        </div>
      </Card>

      {/* Modal de progreso */}
      <ProgressModal isOpen={loading} steps={progressSteps} />

      {/* Modal de error */}
      <Modal
        isOpen={showErrorModal}
        onClose={closeErrorModal}
        title="Error en la consulta"
        footer={<Button onClick={closeErrorModal}>Cerrar</Button>}
      >
        <div className="flex flex-col items-center gap-4 py-6">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-destructive/10 rounded-full">
            <XCircle className="w-8 h-8 text-destructive" />
          </div>
          <div className="text-center">
            <h3 className="text-lg font-semibold text-foreground mb-2">
              No se pudo completar la consulta
            </h3>
            <p className="text-muted-foreground">{error}</p>
          </div>
        </div>
      </Modal>
    </>
  );
}
