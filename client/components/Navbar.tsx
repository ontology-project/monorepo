import React from 'react';
import { Box, Button, Flex, Text } from '@chakra-ui/react';
import { useRouter } from 'next/router';

interface NavBarProps {
  username: string;
  logout: any;
}

const NavBar: React.FC<NavBarProps> = ({ username, logout }) => {
  const router = useRouter();

  return (
    <Flex bg="purple.500" color="white" padding="4" justifyContent="space-between" alignItems="center">
      <Text fontSize="lg" fontWeight="bold">Ontology Project</Text>
      <Flex alignItems="center">
        <Text marginRight="8">Welcome, {username}!</Text>
        <Button onClick={logout}>Logout</Button>
      </Flex>
    </Flex>
  );
};

export default NavBar;