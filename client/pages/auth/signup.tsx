import React, { useState, ChangeEvent, FormEvent } from 'react';
import axios from 'axios';
import { useRouter } from 'next/router';
import {
  Flex,
  Heading,
  Input,
  Button,
  InputGroup,
  Stack,
  InputLeftElement,
  chakra,
  Box,
  Link,
  Avatar,
  FormControl,
  InputRightElement,
  Tab,
  TabList,
  Tabs,
} from "@chakra-ui/react";
import { FaUserAlt, FaLock } from "react-icons/fa";
import { BASE_URL } from '../../utils/constants';

interface Credentials {
  username: string;
  password: string;
  is_kaprodi: boolean;
}

const CFaUserAlt = chakra(FaUserAlt);
const CFaLock = chakra(FaLock);

export default function Signup() {
  const [credentials, setCredentials] = useState<Credentials>({ username: '', password: '', is_kaprodi: true });
  const [showPassword, setShowPassword] = useState(false);
  const router = useRouter();

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setCredentials(prevCredentials => ({
      ...prevCredentials,
      [name]: value,
    }));
  };

  const handleRoleChange = (index: number) => {
    const is_kaprodi = index === 0;
    setCredentials(prevCredentials => ({
      ...prevCredentials,
      is_kaprodi: is_kaprodi,
    }));
  };

  const handleShowClick = () => setShowPassword(!showPassword);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    try {
      console.log("creds", credentials)
      await axios.post(`${BASE_URL}/user/auth/users/`, credentials);
      alert('Signup successful!');
      router.push('/auth/login');
    } catch (error: any) {
      console.error('Signup error:', error);
      if (error.response && error.response.data) {
        let errors = error.response.data;
        let errorMessages = [];
        for (let key in errors) {
          if (Array.isArray(errors[key])) {
            errorMessages.push(`${key}: ${errors[key].join(', ')}`);
          } else {
            errorMessages.push(`${key}: ${errors[key]}`);
          }
        }
        alert('Signup failed! ' + errorMessages.join('\n'));
      } else {
        alert('Signup failed!');
      }
    }
  };

  return (
    <Flex
      flexDirection="column"
      width="100wh"
      height="100vh"
      backgroundColor="gray.200"
      justifyContent="center"
      alignItems="center"
    >
      <Stack
        flexDir="column"
        mb="2"
        justifyContent="center"
        alignItems="center"
      >
        <Avatar bg="purple.500" />
        <Heading color="purple.400">Create Account</Heading>
        <Box minW={{ base: "90%", md: "468px" }}>
          <form onSubmit={handleSubmit}>
            <Stack
              spacing={4}
              p="1rem"
              backgroundColor="whiteAlpha.900"
              boxShadow="md"
            >
              <FormControl>
                <InputGroup>
                  <InputLeftElement pointerEvents="none">
                    <CFaUserAlt color="gray.300" />
                  </InputLeftElement>
                  <Input
                    type="text"
                    placeholder="Username"
                    name="username"
                    value={credentials.username}
                    onChange={handleChange}
                  />
                </InputGroup>
              </FormControl>
              <FormControl>
                <InputGroup>
                  <InputLeftElement
                    pointerEvents="none"
                    color="gray.300"
                  >
                    <CFaLock color="gray.300" />
                  </InputLeftElement>
                  <Input
                    type={showPassword ? "text" : "password"}
                    placeholder="Password"
                    name="password"
                    value={credentials.password}
                    onChange={handleChange}
                  />
                  <InputRightElement width="4.5rem">
                    <Button h="1.75rem" size="sm" onClick={handleShowClick}>
                      {showPassword ? "Hide" : "Show"}
                    </Button>
                  </InputRightElement>
                </InputGroup>
              </FormControl>
              <Box>
                <Tabs index={credentials.is_kaprodi ? 0 : 1} onChange={handleRoleChange} variant="soft-rounded">
                  <TabList>
                    <Tab flex="1" textAlign="center">Kaprodi</Tab>
                    <Tab flex="1" textAlign="center">Reviewer</Tab>
                  </TabList>
                </Tabs>
              </Box>
              <Button
                borderRadius={0}
                type="submit"
                variant="solid"
                width="full"
              >
                Sign Up
              </Button>
            </Stack>
          </form>
        </Box>
      </Stack>
      <Box>
        Already have an account?{" "}
        <Link color="purple.500" href="/auth/login">
          Log In
        </Link>
      </Box>
    </Flex>
  );
}
