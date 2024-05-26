  import "../styles/globals.css";
  import type { AppProps } from "next/app";
  import { ChakraProvider } from "@chakra-ui/react";
  import { customTheme } from "../themes/index";
  import { logout, useAuth } from "../utils/util";
  import NavBar from "../components/Navbar";
  import { useRouter } from "next/router";

  function MyApp({ Component, pageProps }: AppProps) {
    const { isLoggedIn, username, isKaprodi, updateAuthStatus } = useAuth();
    const router = useRouter();
  
    return (
      <ChakraProvider theme={customTheme}>
        {isLoggedIn && <NavBar username={username} isKaprodi={isKaprodi} logout={() => logout(updateAuthStatus, router)} />}
        <Component {...pageProps}/>
      </ChakraProvider>
    );
  }

  export default MyApp;
