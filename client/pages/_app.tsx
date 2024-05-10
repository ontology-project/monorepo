import "../styles/globals.css";
import type { AppProps } from "next/app";
import { ChakraProvider } from "@chakra-ui/react";
import { customTheme } from "../themes/index";
import { logout, useAuth } from "../utils/util";
import NavBar from "../components/Util/Navbar";

function MyApp({ Component, pageProps }: AppProps) {
  const { isLoggedIn, username } = useAuth();
  return (
    <ChakraProvider theme={customTheme}>
      {isLoggedIn && <NavBar username={username} />}
      <Component {...pageProps} />
    </ChakraProvider>
  );
}

export default MyApp;
