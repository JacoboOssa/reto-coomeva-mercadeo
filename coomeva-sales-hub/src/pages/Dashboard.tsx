import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { supabase } from "@/integrations/supabase/client";
import { LoadingSpinner } from "@/components/ui/loading-spinner";
import { Header } from "@/components/dashboard/Header";
import { ConsultCard } from "@/components/dashboard/ConsultCard";
import { ClusterCard } from "@/components/dashboard/ClusterCard";
import { ArchetypeCard } from "@/components/dashboard/ArchetypeCard";
import { ClientProfileResult } from "@/components/dashboard/ClientProfileResult";
import { ArchetypeProfileResult } from "@/components/dashboard/ArchetypeProfileResult";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { X, Search } from "lucide-react";
import type { User } from "@supabase/supabase-js";

interface ClientProfileData {
  arquetipo_y_perfil: string;
  mensaje: string;
  idea: string;
  canal: string;
  recomendacion: string;
}

export default function Dashboard() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [clientProfile, setClientProfile] = useState<ClientProfileData | null>(null);
  const [archetypeProfile, setArchetypeProfile] = useState<any | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    // Check authentication
    supabase.auth.getSession().then(({ data: { session } }) => {
      if (!session) {
        navigate("/auth");
      } else {
        setUser(session.user);
        setLoading(false);
      }
    });

    const { data: { subscription } } = supabase.auth.onAuthStateChange((event, session) => {
      if (!session) {
        navigate("/auth");
      } else {
        setUser(session.user);
      }
    });

    return () => subscription.unsubscribe();
  }, [navigate]);

  const handleClientProfileResult = (data: ClientProfileData) => {
    setClientProfile(data);
    setArchetypeProfile(null);
  };

  const handleArchetypeProfileResult = (data: any) => {
    setArchetypeProfile(data);
    setClientProfile(null);
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background flex flex-col">
      <Header userEmail={user?.email} />
      
      <main className="flex-1 px-6 py-4">
        <div className="h-full animate-fade-in">
          {/* Welcome section - más compacto */}
          <div className="mb-4">
            <h2 className="text-2xl font-bold text-foreground">
              Portal de Ventas Coomeva
            </h2>
            <p className="text-sm text-muted-foreground">
              Gestiona la información de tus clientes
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
            {/* Columna izquierda - Formularios */}
            <div className="lg:col-span-1 space-y-4">
              <ConsultCard onResultReady={handleClientProfileResult} />
              <ArchetypeCard onResult={handleArchetypeProfileResult} />
              <ClusterCard />
            </div>

            {/* Columna derecha - Resultados */}
            <div className="lg:col-span-2">
              {clientProfile ? (
                <Card className="p-5 relative animate-fade-in max-h-[calc(100vh-140px)] overflow-y-auto">
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={() => setClientProfile(null)}
                    className="sticky top-2 right-2 ml-auto h-8 w-8 rounded-full hover:bg-destructive/10 z-10 float-right"
                  >
                    <X className="h-4 w-4" />
                  </Button>
                  <ClientProfileResult data={clientProfile} />
                </Card>
              ) : archetypeProfile ? (
                <Card className="p-5 relative animate-fade-in max-h-[calc(100vh-140px)] overflow-y-auto">
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={() => setArchetypeProfile(null)}
                    className="sticky top-2 right-2 ml-auto h-8 w-8 rounded-full hover:bg-destructive/10 z-10 float-right"
                  >
                    <X className="h-4 w-4" />
                  </Button>
                  <ArchetypeProfileResult data={archetypeProfile} />
                </Card>
              ) : (
                <Card className="p-8 h-[calc(100vh-140px)] flex items-center justify-center border-dashed">
                  <div className="text-center space-y-2">
                    <div className="inline-flex items-center justify-center w-14 h-14 bg-muted rounded-full mb-1">
                      <Search className="w-7 h-7 text-muted-foreground" />
                    </div>
                    <h3 className="text-lg font-semibold text-muted-foreground">
                      Realiza una consulta
                    </h3>
                    <p className="text-xs text-muted-foreground max-w-sm">
                      Ingresa el número de cédula del cliente para ver su perfil y recomendaciones personalizadas
                    </p>
                  </div>
                </Card>
              )}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
