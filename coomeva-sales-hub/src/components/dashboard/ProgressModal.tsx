import { Modal } from "@/components/ui/modal";
import { LoadingSpinner } from "@/components/ui/loading-spinner";
import { CheckCircle2, Loader2 } from "lucide-react";

interface ProgressStep {
  label: string;
  completed: boolean;
}

interface ProgressModalProps {
  isOpen: boolean;
  steps: ProgressStep[];
}

export function ProgressModal({ isOpen, steps }: ProgressModalProps) {
  return (
    <Modal
      isOpen={isOpen}
      onClose={() => {}} // No se puede cerrar manualmente
      title="Procesando Consulta"
    >
      <div className="space-y-6 py-4">
        <div className="flex flex-col items-center gap-4 mb-6">
          <LoadingSpinner size="lg" />
          <p className="text-sm text-muted-foreground text-center">
            Por favor espera mientras procesamos la información...
          </p>
        </div>

        <div className="space-y-4">
          {steps.map((step, index) => (
            <div
              key={index}
              className={`flex items-center gap-3 p-3 rounded-lg transition-all ${
                step.completed
                  ? "bg-primary/10 border border-primary/20"
                  : "bg-muted/30"
              }`}
            >
              {step.completed ? (
                <CheckCircle2 className="w-5 h-5 text-primary flex-shrink-0" />
              ) : (
                <Loader2 className="w-5 h-5 text-muted-foreground animate-spin flex-shrink-0" />
              )}
              <span
                className={`text-sm font-medium ${
                  step.completed ? "text-primary" : "text-muted-foreground"
                }`}
              >
                {step.label}
              </span>
            </div>
          ))}
        </div>
      </div>
    </Modal>
  );
}
