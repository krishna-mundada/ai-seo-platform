import { AppShell, Burger, Group, Text, NavLink, ScrollArea, Button } from '@mantine/core'
import { useDisclosure } from '@mantine/hooks'
import { Routes, Route, useLocation, Link } from 'react-router-dom'
import { 
  IconDashboard, 
  IconFileText, 
  IconBuildingStore, 
  IconSpeakerphone, 
  IconSettings,
  IconSparkles
} from '@tabler/icons-react'
import { SignedIn, SignedOut, SignInButton, UserButton } from '@clerk/clerk-react'
import { Dashboard } from './pages/Dashboard'
import { ContentGenerator } from './pages/ContentGenerator'
import { ContentList } from './pages/ContentList'
import { BusinessManagement } from './pages/BusinessManagement'

const navigationItems = [
  { icon: IconDashboard, label: 'Dashboard', link: '/' },
  { icon: IconSparkles, label: 'Generate Content', link: '/generate' },
  { icon: IconFileText, label: 'Content', link: '/content' },
  { icon: IconBuildingStore, label: 'Businesses', link: '/businesses' },
  { icon: IconSpeakerphone, label: 'Campaigns', link: '/campaigns' },
  { icon: IconSettings, label: 'Settings', link: '/settings' },
]

export default function App() {
  const [opened, { toggle }] = useDisclosure()
  const location = useLocation()

  return (
    <>
      {/* Show sign-in UI when user is not authenticated */}
      <SignedOut>
        <div style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          height: '100vh',
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          color: 'white'
        }}>
          <Group mb="xl">
            <IconSparkles size={48} />
            <Text size="3rem" fw={700}>
              AI SEO Platform
            </Text>
          </Group>
          <Text size="xl" mb="xl" ta="center" c="dimmed">
            Generate AI-powered content for your business
          </Text>
          <SignInButton>
            <Button size="lg" variant="white" color="dark">
              Sign In to Continue
            </Button>
          </SignInButton>
        </div>
      </SignedOut>

      {/* Show main app when user is authenticated */}
      <SignedIn>
        <AppShell
          header={{ height: 60 }}
          navbar={{
            width: 280,
            breakpoint: 'sm',
            collapsed: { mobile: !opened },
          }}
          padding="md"
        >
          <AppShell.Header>
            <Group h="100%" px="md" justify="space-between">
              <Group>
                <Burger opened={opened} onClick={toggle} hiddenFrom="sm" size="sm" />
                <Group>
                  <IconSparkles size={28} style={{ color: 'var(--mantine-color-blue-6)' }} />
                  <Text size="xl" fw={700} c="blue">
                    AI SEO Platform
                  </Text>
                </Group>
              </Group>
              <UserButton 
                appearance={{
                  elements: {
                    avatarBox: "w-8 h-8"
                  }
                }}
              />
            </Group>
          </AppShell.Header>

          <AppShell.Navbar p="md">
            <AppShell.Section grow my="md" component={ScrollArea}>
              {navigationItems.map((item) => (
                <NavLink
                  key={item.label}
                  component={Link}
                  to={item.link}
                  label={item.label}
                  leftSection={<item.icon size={20} />}
                  active={location.pathname === item.link}
                  variant="subtle"
                  mb="xs"
                />
              ))}
            </AppShell.Section>
          </AppShell.Navbar>

          <AppShell.Main>
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/generate" element={<ContentGenerator />} />
              <Route path="/content" element={<ContentList />} />
              <Route path="/businesses" element={<BusinessManagement />} />
              <Route path="/campaigns" element={<div>Campaigns (Coming Soon)</div>} />
              <Route path="/settings" element={<div>Settings (Coming Soon)</div>} />
            </Routes>
          </AppShell.Main>
        </AppShell>
      </SignedIn>
    </>
  )
}
