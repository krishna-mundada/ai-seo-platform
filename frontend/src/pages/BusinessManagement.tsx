import { 
  Stack, 
  Text, 
  Card, 
  Group, 
  Button, 
  Badge,
  Grid,
  ActionIcon,
  Modal,
  TextInput,
  Textarea,
  Select,
  Combobox,
  Input,
  InputBase,
  useCombobox,
  LoadingOverlay
} from '@mantine/core'
import { useDisclosure } from '@mantine/hooks'
import { useForm } from '@mantine/form'
import { IconPlus, IconEdit, IconTrash, IconBuildingStore } from '@tabler/icons-react'
import React, { useState, useEffect } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { businessApi, industryApi } from '../lib/api'
import { notifications } from '@mantine/notifications'
import styles from '../components/CenteredModal.module.css'

interface Business {
  id: number
  name: string
  industry?: string
  description?: string
  website_url?: string
  target_audience?: string
  brand_voice?: string
  created_at: string
}

interface Industry {
  id: number
  name: string
  slug: string
  icon?: string
  color?: string
  is_active: boolean
}

export function BusinessManagement() {
  const [opened, { open, close }] = useDisclosure(false)
  const [editingBusiness, setEditingBusiness] = useState<Business | null>(null)
  const queryClient = useQueryClient()
  const combobox = useCombobox({
    onDropdownClose: () => combobox.resetSelectedOption(),
  })

  // Fetch businesses
  const { data: businesses = [], isLoading } = useQuery({
    queryKey: ['businesses'],
    queryFn: () => businessApi.list().then(res => res.data),
  })

  // Fetch industries
  const { data: industries = [], isLoading: industriesLoading, error: industriesError } = useQuery({
    queryKey: ['industries'],
    queryFn: () => industryApi.list({ active_only: true }).then(res => res.data),
  })

  const form = useForm({
    initialValues: {
      name: '',
      industry: '',
      description: '',
      website_url: '',
      target_audience: '',
      brand_voice: '',
    },
    validate: {
      name: (value) => (!value ? 'Business name is required' : null),
      industry: (value) => (!value ? 'Industry is required' : null),
      description: (value) => (!value ? 'Description is required' : null),
    },
  })

  // Create business mutation
  const createMutation = useMutation({
    mutationFn: businessApi.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['businesses'] })
      notifications.show({
        title: 'Success',
        message: 'Business created successfully',
        color: 'green',
      })
      close()
    },
    onError: () => {
      notifications.show({
        title: 'Error',
        message: 'Failed to create business',
        color: 'red',
      })
    },
  })

  // Update business mutation
  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: number, data: any }) => businessApi.update(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['businesses'] })
      notifications.show({
        title: 'Success',
        message: 'Business updated successfully',
        color: 'green',
      })
      close()
    },
    onError: () => {
      notifications.show({
        title: 'Error',
        message: 'Failed to update business',
        color: 'red',
      })
    },
  })

  // Delete business mutation
  const deleteMutation = useMutation({
    mutationFn: businessApi.delete,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['businesses'] })
      notifications.show({
        title: 'Success',
        message: 'Business deleted successfully',
        color: 'green',
      })
    },
    onError: () => {
      notifications.show({
        title: 'Error',
        message: 'Failed to delete business',
        color: 'red',
      })
    },
  })

  const handleEdit = (business: Business) => {
    setEditingBusiness(business)
    form.setValues({
      name: business.name,
      industry: business.industry || '',
      description: business.description || '',
      website_url: business.website_url || '',
      target_audience: business.target_audience || '',
      brand_voice: business.brand_voice || '',
    })
    open()
  }

  const handleNew = () => {
    setEditingBusiness(null)
    form.reset()
    open()
  }

  const handleSubmit = (values: typeof form.values) => {
    if (editingBusiness) {
      updateMutation.mutate({ id: editingBusiness.id, data: values })
    } else {
      createMutation.mutate({ ...values, owner_id: 1 }) // TODO: Use actual user ID
    }
  }

  const handleDelete = (id: number) => {
    const confirmed = confirm(
      'Are you sure you want to delete this business?\n\n' +
      'This will also delete all associated content (blog posts, social media posts, etc.). ' +
      'This action cannot be undone.'
    )
    if (confirmed) {
      deleteMutation.mutate(id)
    }
  }

  return (
    <Stack gap="lg">
      <Group justify="space-between">
        <Text size="xl" fw={700}>
          Business Management
        </Text>
        <Button leftSection={<IconPlus size={16} />} onClick={handleNew}>
          Add Business
        </Button>
      </Group>

      <LoadingOverlay visible={isLoading} />
      
      {businesses.length === 0 ? (
        <Card shadow="sm" padding="xl" radius="md" withBorder>
          <Stack align="center" gap="md">
            <IconBuildingStore size={48} color="gray" />
            <Text size="lg" fw={500} c="dimmed">
              No businesses yet
            </Text>
            <Text size="sm" c="dimmed" ta="center">
              Create your first business profile to start generating AI content
            </Text>
            <Button leftSection={<IconPlus size={16} />} onClick={handleNew}>
              Add Your First Business
            </Button>
          </Stack>
        </Card>
      ) : (
        <Grid>
          {businesses.map((business) => (
            <Grid.Col span={{ base: 12, sm: 6, xl: 4 }} key={business.id}>
              <Card shadow="sm" padding="lg" radius="md" withBorder h="100%" style={{ minHeight: 280 }}>
                <Stack gap="md" h="100%">
                  <Group justify="space-between">
                    <Group>
                      <IconBuildingStore size={20} color="blue" />
                      <Text fw={600} size="lg">
                        {business.name}
                      </Text>
                    </Group>
                    <Badge variant="light" size="sm">
                      {business.industry || 'Not specified'}
                    </Badge>
                  </Group>

                  <Text size="sm" c="dimmed" style={{ flex: 1 }}>
                    {business.description || 'No description available'}
                  </Text>

                  <Stack gap="xs">
                    {business.website_url && (
                      <Group justify="space-between">
                        <Text size="xs" c="dimmed">Website:</Text>
                        <Text 
                          size="xs" 
                          c="blue" 
                          td="underline"
                          style={{ cursor: 'pointer' }}
                          onClick={() => window.open(business.website_url, '_blank')}
                        >
                          {business.website_url}
                        </Text>
                      </Group>
                    )}
                    
                    {business.target_audience && (
                      <Group justify="space-between">
                        <Text size="xs" c="dimmed">Target:</Text>
                        <Text size="xs">
                          {business.target_audience}
                        </Text>
                      </Group>
                    )}
                    
                    {business.brand_voice && (
                      <Group justify="space-between">
                        <Text size="xs" c="dimmed">Voice:</Text>
                        <Text size="xs">
                          {business.brand_voice}
                        </Text>
                      </Group>
                    )}

                    <Group justify="space-between">
                      <Text size="xs" c="dimmed">Created:</Text>
                      <Text size="xs">
                        {new Date(business.created_at).toLocaleDateString()}
                      </Text>
                    </Group>
                  </Stack>

                  <Group gap="xs" mt="auto">
                    <ActionIcon 
                      variant="light" 
                      size="sm"
                      onClick={() => handleEdit(business)}
                    >
                      <IconEdit size={16} />
                    </ActionIcon>
                    <ActionIcon 
                      variant="light" 
                      size="sm" 
                      color="red"
                      onClick={() => handleDelete(business.id)}
                      loading={deleteMutation.isPending}
                    >
                      <IconTrash size={16} />
                    </ActionIcon>
                  </Group>
                </Stack>
              </Card>
            </Grid.Col>
          ))}
        </Grid>
      )}

      <Modal 
        opened={opened} 
        onClose={close} 
        title={editingBusiness ? 'Edit Business' : 'Add New Business'}
        centered
        size="lg"
        classNames={{
          inner: styles.modalInner,
          content: styles.modalContent,
          overlay: styles.modalOverlay,
        }}
      >
        <form onSubmit={form.onSubmit(handleSubmit)}>
          <Stack gap="md">
            <TextInput
              label="Business Name"
              placeholder="Enter business name"
              {...form.getInputProps('name')}
              required
            />

            <Combobox
              store={combobox}
              withinPortal={false}
            >
              <Combobox.Target>
                <InputBase
                  component="button"
                  type="button"
                  pointer
                  rightSection={<Combobox.Chevron />}
                  onClick={() => combobox.toggleDropdown()}
                  rightSectionPointerEvents="none"
                  label="Industry"
                  placeholder={industriesLoading ? "Loading industries..." : "Select industry"}
                  required
                  disabled={industriesLoading}
                >
                  {form.values.industry}
                </InputBase>
              </Combobox.Target>

              <Combobox.Dropdown>
                <Combobox.Options>
                  {Array.isArray(industries) ? industries.map((industry: Industry) => (
                    <Combobox.Option 
                      value={industry.name} 
                      key={industry.id}
                      onClick={() => {
                        form.setFieldValue('industry', industry.name)
                        combobox.closeDropdown()
                      }}
                    >
                      {industry.icon ? `${industry.icon} ${industry.name}` : industry.name}
                    </Combobox.Option>
                  )) : null}
                </Combobox.Options>
              </Combobox.Dropdown>
            </Combobox>

            <Textarea
              label="Description"
              placeholder="Describe your business"
              rows={3}
              {...form.getInputProps('description')}
              required
            />

            <TextInput
              label="Website URL"
              placeholder="https://example.com"
              {...form.getInputProps('website_url')}
            />

            <Textarea
              label="Target Audience"
              placeholder="Describe your target audience"
              rows={2}
              {...form.getInputProps('target_audience')}
            />

            <Textarea
              label="Brand Voice"
              placeholder="Describe your brand voice and tone"
              rows={2}
              {...form.getInputProps('brand_voice')}
            />

            <Group justify="flex-end" gap="sm">
              <Button variant="outline" onClick={close}>
                Cancel
              </Button>
              <Button 
                type="submit"
                loading={createMutation.isPending || updateMutation.isPending}
              >
                {editingBusiness ? 'Update' : 'Create'} Business
              </Button>
            </Group>
          </Stack>
        </form>
      </Modal>
    </Stack>
  )
}