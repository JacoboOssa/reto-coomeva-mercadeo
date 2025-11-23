import { useState } from "react";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Users, Loader2 } from "lucide-react";
import { useToast } from "@/hooks/use-toast";

const WEBHOOK_URL = "https://jacobossaguarnizoo19.app.n8n.cloud/webhook-test/e0d3199e-1b27-4ee7-8787-56f7e0ef680f";

const ARQUETIPOS = [
  "Aportante promedio con perfil financiero moderado",
  "Aportante vulnerable con alta carga crediticia",
  "Aportante consolidado con alta estabilidad y bajo riesgo",
  "Profesional joven con desempeño financiero estable",
  "Aportante de bajos ingresos y limitada capacidad de ahorro",
];

interface ArchetypeCardProps {
  onResult: (data: any) => void;
}

export function ArchetypeCard({ onResult }: ArchetypeCardProps) {
  const [arquetipo, setArquetipo] = useState("");
  const [producto, setProducto] = useState("");
  const [loading, setLoading] = useState(false);
  const { toast } = useToast();

  const handleConsult = async () => {
    if (!arquetipo || !producto.trim()) {
      toast({
        variant: "destructive",
        title: "Campos requeridos",
        description: "Por favor, selecciona un arquetipo e ingresa un producto.",
      });
      return;
    }

    setLoading(true);

    try {
      const response = await fetch(WEBHOOK_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          opcion: "3",
          arquetipo: arquetipo,
          producto: producto.trim(),
        }),
      });

      if (!response.ok) {
        throw new Error(`Error ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      
      toast({
        title: "Consulta exitosa",
        description: "La consulta por arquetipo ha sido procesada.",
      });

      // Pasar los resultados al componente padre con metadatos
      onResult({
        ...data,
        _metadata: {
          arquetipo,
          producto
        }
      });

      // Limpiar formulario
      setArquetipo("");
      setProducto("");
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "Error desconocido";
      toast({
        variant: "destructive",
        title: "Error en la consulta",
        description: errorMessage,
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card className="p-5 hover:shadow-lg transition-all bg-gradient-to-br from-card to-secondary/30">
      <div className="space-y-4">
        <div className="flex items-center gap-3">
          <div className="inline-flex items-center justify-center w-11 h-11 bg-primary/10 rounded-xl">
            <Users className="w-6 h-6 text-primary" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-foreground">Consultar por Arquetipo</h2>
            <p className="text-xs text-muted-foreground">
              Busca información por perfil
            </p>
          </div>
        </div>

        <div className="space-y-2">
          <Label htmlFor="arquetipo" className="text-sm font-medium">
            Arquetipo
          </Label>
          <Select value={arquetipo} onValueChange={setArquetipo} disabled={loading}>
            <SelectTrigger id="arquetipo" className="h-11">
              <SelectValue placeholder="Selecciona un arquetipo" />
            </SelectTrigger>
            <SelectContent>
              {ARQUETIPOS.map((arq) => (
                <SelectItem key={arq} value={arq}>
                  {arq}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
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
          {loading ? (
            <>
              <Loader2 className="w-5 h-5 mr-2 animate-spin" />
              Consultando...
            </>
          ) : (
            <>
              <Users className="w-5 h-5 mr-2" />
              Consultar
            </>
          )}
        </Button>
      </div>
    </Card>
  );
}
