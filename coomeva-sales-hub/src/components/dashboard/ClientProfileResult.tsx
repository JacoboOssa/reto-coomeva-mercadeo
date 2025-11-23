import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { 
  User, 
  MessageSquare, 
  Lightbulb, 
  Radio, 
  Target,
  CheckCircle2
} from "lucide-react";

interface ClientProfileData {
  arquetipo_y_perfil: string;
  mensaje: string;
  idea: string;
  canal: string;
  recomendacion: string;
}

interface ClientProfileResultProps {
  data: ClientProfileData;
}

export function ClientProfileResult({ data }: ClientProfileResultProps) {
  return (
    <div className="space-y-4">
      {/* Header principal */}
      <div className="text-center pb-3 border-b border-border">
        <div className="inline-flex items-center justify-center w-14 h-14 bg-primary/10 rounded-full mb-2">
          <CheckCircle2 className="w-7 h-7 text-primary" />
        </div>
        <h3 className="text-2xl font-bold text-foreground mb-1">Análisis del Cliente</h3>
        <p className="text-sm text-muted-foreground">
          Información procesada lista para tu estrategia comercial
        </p>
      </div>

      {/* Arquetipo y Perfil */}
      <Card className="p-5 bg-gradient-to-br from-blue-50 to-blue-100/50 dark:from-blue-950/30 dark:to-blue-900/20 border-blue-200 dark:border-blue-800">
        <div className="flex items-start gap-3">
          <div className="inline-flex items-center justify-center w-9 h-9 bg-blue-500/10 rounded-lg flex-shrink-0">
            <User className="w-5 h-5 text-blue-600 dark:text-blue-400" />
          </div>
          <div className="flex-1 space-y-2">
            <div className="flex items-center gap-2 flex-wrap">
              <h4 className="text-base font-semibold text-foreground">Arquetipo y Perfil</h4>
              <Badge variant="secondary" className="bg-blue-500/10 text-blue-700 dark:text-blue-300">
                Análisis
              </Badge>
            </div>
            <p className="text-sm text-muted-foreground leading-relaxed">
              {data.arquetipo_y_perfil}
            </p>
          </div>
        </div>
      </Card>

      {/* Idea Principal */}
      <Card className="p-5 bg-gradient-to-br from-amber-50 to-amber-100/50 dark:from-amber-950/30 dark:to-amber-900/20 border-amber-200 dark:border-amber-800">
        <div className="flex items-start gap-3">
          <div className="inline-flex items-center justify-center w-9 h-9 bg-amber-500/10 rounded-lg flex-shrink-0">
            <Lightbulb className="w-5 h-5 text-amber-600 dark:text-amber-400" />
          </div>
          <div className="flex-1 space-y-2">
            <div className="flex items-center gap-2 flex-wrap">
              <h4 className="text-base font-semibold text-foreground">Propuesta de Valor</h4>
              <Badge variant="secondary" className="bg-amber-500/10 text-amber-700 dark:text-amber-300">
                Idea
              </Badge>
            </div>
            <p className="text-sm text-muted-foreground leading-relaxed italic">
              "{data.idea}"
            </p>
          </div>
        </div>
      </Card>

      {/* Mensaje Sugerido */}
      <Card className="p-5 bg-gradient-to-br from-purple-50 to-purple-100/50 dark:from-purple-950/30 dark:to-purple-900/20 border-purple-200 dark:border-purple-800">
        <div className="flex items-start gap-3">
          <div className="inline-flex items-center justify-center w-9 h-9 bg-purple-500/10 rounded-lg flex-shrink-0">
            <MessageSquare className="w-5 h-5 text-purple-600 dark:text-purple-400" />
          </div>
          <div className="flex-1 space-y-2">
            <div className="flex items-center gap-2 flex-wrap">
              <h4 className="text-base font-semibold text-foreground">Enfoque del Mensaje</h4>
              <Badge variant="secondary" className="bg-purple-500/10 text-purple-700 dark:text-purple-300">
                Comunicación
              </Badge>
            </div>
            <p className="text-sm text-muted-foreground leading-relaxed">
              {data.mensaje}
            </p>
          </div>
        </div>
      </Card>

      {/* Canal Recomendado */}
      <Card className="p-5 bg-gradient-to-br from-green-50 to-green-100/50 dark:from-green-950/30 dark:to-green-900/20 border-green-200 dark:border-green-800">
        <div className="flex items-start gap-3">
          <div className="inline-flex items-center justify-center w-9 h-9 bg-green-500/10 rounded-lg flex-shrink-0">
            <Radio className="w-5 h-5 text-green-600 dark:text-green-400" />
          </div>
          <div className="flex-1 space-y-2">
            <div className="flex items-center gap-2 flex-wrap">
              <h4 className="text-base font-semibold text-foreground">Canal Preferido</h4>
              <Badge variant="secondary" className="bg-green-500/10 text-green-700 dark:text-green-300">
                Contacto
              </Badge>
            </div>
            <p className="text-sm text-muted-foreground leading-relaxed">
              {data.canal}
            </p>
          </div>
        </div>
      </Card>

      {/* Recomendación Final */}
      <Card className="p-5 bg-gradient-to-br from-rose-50 to-rose-100/50 dark:from-rose-950/30 dark:to-rose-900/20 border-rose-200 dark:border-rose-800">
        <div className="flex items-start gap-3">
          <div className="inline-flex items-center justify-center w-9 h-9 bg-rose-500/10 rounded-lg flex-shrink-0">
            <Target className="w-5 h-5 text-rose-600 dark:text-rose-400" />
          </div>
          <div className="flex-1 space-y-2">
            <div className="flex items-center gap-2 flex-wrap">
              <h4 className="text-base font-semibold text-foreground">Estrategia de Venta</h4>
              <Badge variant="secondary" className="bg-rose-500/10 text-rose-700 dark:text-rose-300">
                Recomendación
              </Badge>
            </div>
            <p className="text-sm text-muted-foreground leading-relaxed">
              {data.recomendacion}
            </p>
          </div>
        </div>
      </Card>

      {/* Footer informativo */}
      <div className="bg-muted/50 rounded-lg p-3 border border-border">
        <p className="text-xs text-muted-foreground text-center leading-relaxed">
          💡 Información generada automáticamente. Úsala como guía para personalizar tu aproximación comercial.
        </p>
      </div>
    </div>
  );
}
