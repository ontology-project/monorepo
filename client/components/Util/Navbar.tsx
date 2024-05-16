// components/NavBar.tsx
import React from 'react';
import { Box, Button, Flex, Text } from '@chakra-ui/react';
import { useRouter } from 'next/router';
import { logout } from '../../utils/util';

interface NavBarProps {
  username: string;
}

const NavBar: React.FC<NavBarProps> = ({ username }) => {
  const router = useRouter();

  return (
    <Flex bg="teal.500" color="white" padding="4" justifyContent="space-between" alignItems="center">
      <Text fontSize="lg" fontWeight="bold">Ontology Project</Text>
      <Flex alignItems="center">
        <Text marginRight="8">Welcome, {username}!</Text>
        <Button colorScheme="teal" variant="outline" onClick={() => logout(router)}>Logout</Button>
      </Flex>
    </Flex>
  );
};

export default NavBar;
