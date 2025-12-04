import { useEffect } from "react";
import { useRouter } from "next/router";

export default function HomePage() {
  const router = useRouter();

  useEffect(() => {
    // Redirect to /Campaign on page load
    router.push("/Campaign");
  }, [router]);

  return (
    <div className="page">
      <main className="container">
        <p>Redirecting to Campaign page...</p>
      </main>
    </div>
  );
}



