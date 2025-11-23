import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Target, MessageSquare, Phone, ShieldAlert, Star, User, Package } from "lucide-react";

interface ArchetypeProfileData {
  match_producto_perfil: {
    score_afinidad: number;
    analisis_viabilidad: string;
    angulo_venta: string;
  };
  estrategia_comunicacion: {
    canal_recomendado?: string;
    canales_sugeridos?: string[];
    justificacion_canal?: string;
    justificacion_medios?: string;
    mejor_momento: string;
    tono_voz: string;
  };
  kit_ventas: {
    mensaje_whatsapp_o_asunto: string;
    argumento_apertura: string;
    argumento_cierre: string;
  };
  manejo_resistencias: {
    posible_objecion: string;
    respuesta_inteligente: string;
  };
  _metadata?: {
    arquetipo: string;
    producto: string;
  };
}

interface ArchetypeProfileResultProps {
  data: ArchetypeProfileData;
}

export function ArchetypeProfileResult({ data }: ArchetypeProfileResultProps) {
  return (
    <div className="space-y-6 animate-fade-in">
      {/* Header */}
      <div className="text-center space-y-2">
        <h3 className="text-2xl font-bold text-foreground">Análisis por Arquetipo</h3>
        <p className="text-sm text-muted-foreground">Estrategia comercial personalizada</p>
      </div>

      {/* Información de la Consulta */}
      {data._metadata && (
        <Card className="p-4 bg-gradient-to-br from-muted/50 to-muted/20">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="flex items-start gap-3">
              <div className="inline-flex items-center justify-center w-10 h-10 bg-primary/10 rounded-lg shrink-0">
                <User className="w-5 h-5 text-primary" />
              </div>
              <div>
                <p className="text-xs font-medium text-muted-foreground mb-1">Arquetipo Consultado</p>
                <p className="text-sm font-semibold text-foreground">{data._metadata.arquetipo}</p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <div className="inline-flex items-center justify-center w-10 h-10 bg-secondary/10 rounded-lg shrink-0">
                <Package className="w-5 h-5 text-secondary" />
              </div>
              <div>
                <p className="text-xs font-medium text-muted-foreground mb-1">Producto</p>
                <p className="text-sm font-semibold text-foreground">{data._metadata.producto}</p>
              </div>
            </div>
          </div>
        </Card>
      )}

      {/* Match Producto-Perfil */}
      <Card className="p-6 space-y-4 bg-gradient-to-br from-card to-primary/5">
        <div className="flex items-start gap-4">
          <div className="inline-flex items-center justify-center w-12 h-12 bg-primary/10 rounded-xl shrink-0">
            <Target className="w-6 h-6 text-primary" />
          </div>
          <div className="space-y-3 flex-1">
            <div className="flex items-center justify-between">
              <h4 className="text-lg font-semibold text-foreground">Match Producto-Perfil</h4>
              <Badge variant="secondary" className="text-base px-3">
                <Star className="w-4 h-4 mr-1 inline" />
                {data.match_producto_perfil.score_afinidad}/10
              </Badge>
            </div>
            <div className="space-y-2">
              <div>
                <span className="text-sm font-medium text-muted-foreground">Análisis de Viabilidad:</span>
                <p className="text-base text-foreground mt-1">{data.match_producto_perfil.analisis_viabilidad}</p>
              </div>
              <div>
                <span className="text-sm font-medium text-muted-foreground">Ángulo de Venta:</span>
                <p className="text-base text-foreground mt-1">{data.match_producto_perfil.angulo_venta}</p>
              </div>
            </div>
          </div>
        </div>
      </Card>

      {/* Estrategia de Comunicación */}
      <Card className="p-6 space-y-4 bg-gradient-to-br from-card to-secondary/5">
        <div className="flex items-start gap-4">
          <div className="inline-flex items-center justify-center w-12 h-12 bg-secondary/10 rounded-xl shrink-0">
            <Phone className="w-6 h-6 text-secondary" />
          </div>
          <div className="space-y-3 flex-1">
            <h4 className="text-lg font-semibold text-foreground">Estrategia de Comunicación</h4>
            <div className="grid gap-3">
              <div className="flex flex-wrap items-center gap-2">
                {data.estrategia_comunicacion.canales_sugeridos ? (
                  data.estrategia_comunicacion.canales_sugeridos.map((canal, idx) => (
                    <Badge key={idx} variant="outline">{canal}</Badge>
                  ))
                ) : (
                  <Badge variant="outline">{data.estrategia_comunicacion.canal_recomendado}</Badge>
                )}
                <span className="text-sm text-muted-foreground">•</span>
                <span className="text-sm text-muted-foreground">Mejor momento: {data.estrategia_comunicacion.mejor_momento}</span>
              </div>
              <div>
                <span className="text-sm font-medium text-muted-foreground">Justificación:</span>
                <p className="text-base text-foreground mt-1">
                  {data.estrategia_comunicacion.justificacion_medios || data.estrategia_comunicacion.justificacion_canal}
                </p>
              </div>
              <div>
                <span className="text-sm font-medium text-muted-foreground">Tono de Voz:</span>
                <p className="text-base text-foreground mt-1">{data.estrategia_comunicacion.tono_voz}</p>
              </div>
            </div>
          </div>
        </div>
      </Card>

      {/* Kit de Ventas */}
      <Card className="p-6 space-y-4 bg-gradient-to-br from-card to-accent/5">
        <div className="flex items-start gap-4">
          <div className="inline-flex items-center justify-center w-12 h-12 bg-accent/10 rounded-xl shrink-0">
            <MessageSquare className="w-6 h-6 text-accent" />
          </div>
          <div className="space-y-3 flex-1">
            <h4 className="text-lg font-semibold text-foreground">Kit de Ventas</h4>
            <div className="space-y-3">
              <div className="p-4 bg-muted/50 rounded-lg">
                <span className="text-sm font-medium text-muted-foreground">Mensaje/Asunto:</span>
                <p className="text-base text-foreground mt-1 font-medium">{data.kit_ventas.mensaje_whatsapp_o_asunto}</p>
              </div>
              <div>
                <span className="text-sm font-medium text-muted-foreground">Argumento de Apertura:</span>
                <p className="text-base text-foreground mt-1">{data.kit_ventas.argumento_apertura}</p>
              </div>
              <div>
                <span className="text-sm font-medium text-muted-foreground">Argumento de Cierre:</span>
                <p className="text-base text-foreground mt-1">{data.kit_ventas.argumento_cierre}</p>
              </div>
            </div>
          </div>
        </div>
      </Card>

      {/* Manejo de Resistencias */}
      <Card className="p-6 space-y-4 bg-gradient-to-br from-card to-destructive/5">
        <div className="flex items-start gap-4">
          <div className="inline-flex items-center justify-center w-12 h-12 bg-destructive/10 rounded-xl shrink-0">
            <ShieldAlert className="w-6 h-6 text-destructive" />
          </div>
          <div className="space-y-3 flex-1">
            <h4 className="text-lg font-semibold text-foreground">Manejo de Resistencias</h4>
            <div className="space-y-3">
              <div>
                <span className="text-sm font-medium text-muted-foreground">Posible Objeción:</span>
                <p className="text-base text-foreground mt-1 italic">&ldquo;{data.manejo_resistencias.posible_objecion}&rdquo;</p>
              </div>
              <div className="p-4 bg-muted/50 rounded-lg">
                <span className="text-sm font-medium text-muted-foreground">Respuesta Inteligente:</span>
                <p className="text-base text-foreground mt-1">{data.manejo_resistencias.respuesta_inteligente}</p>
              </div>
            </div>
          </div>
        </div>
      </Card>

      {/* Footer */}
      <div className="text-center pt-4">
        <p className="text-xs text-muted-foreground">
          Análisis generado para optimizar la estrategia comercial
        </p>
      </div>
    </div>
  );
}
