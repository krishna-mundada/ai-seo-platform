import { 
  Table, 
  Badge, 
  Group, 
  Text, 
  ActionIcon, 
  Stack,
  Card,
  Button,
  Select,
  TextInput,
  LoadingOverlay,
  Modal,
  Textarea,
  Box,
  UnstyledButton,
  Center
} from '@mantine/core'
import { IconEye, IconEdit, IconTrash, IconSearch, IconPlus, IconSelector, IconChevronDown, IconChevronUp, IconGripVertical } from '@tabler/icons-react'
import { useState, useMemo } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { contentApi } from '../lib/api'
import { notifications } from '@mantine/notifications'
import { useDisclosure } from '@mantine/hooks'
import { useNavigate } from 'react-router-dom'
import { EditContentModal } from '../components/EditContentModal'

interface Content {
  id: number
  title: string
  content_text: string
  content_type: string
  status: string
  seo_score?: number
  created_at: string
  business?: {
    id: number
    name: string
    industry?: string
  }
  keywords?: string[]
  meta_description?: string
}

type SortField = 'title' | 'content_type' | 'status' | 'seo_score' | 'created_at' | 'business'
type SortDirection = 'asc' | 'desc'

interface TableColumn {
  key: SortField | 'actions'
  label: string
  sortable: boolean
  width: number
  minWidth: number
}

const statusColors = {
  published: 'green',
  pending_approval: 'yellow',
  draft: 'gray',
  rejected: 'red'
}

const contentTypeLabels = {
  blog_post: 'Blog Post',
  linkedin_post: 'LinkedIn',
  twitter_post: 'Twitter',
  facebook_post: 'Facebook',
  instagram_post: 'Instagram',
  email: 'Email'
}

export function ContentList() {
  const navigate = useNavigate()
  const [statusFilter, setStatusFilter] = useState<string | null>(null)
  const [typeFilter, setTypeFilter] = useState<string | null>(null)
  const [search, setSearch] = useState('')
  const [selectedContent, setSelectedContent] = useState<Content | null>(null)
  const [viewOpened, { open: openView, close: closeView }] = useDisclosure(false)
  const [editOpened, { open: openEdit, close: closeEdit }] = useDisclosure(false)
  const [sortField, setSortField] = useState<SortField>('created_at')
  const [sortDirection, setSortDirection] = useState<SortDirection>('desc')
  const [resizing, setResizing] = useState<string | null>(null)
  const [columns, setColumns] = useState<TableColumn[]>([
    { key: 'title', label: 'Title', sortable: true, width: 300, minWidth: 200 },
    { key: 'content_type', label: 'Type', sortable: true, width: 130, minWidth: 100 },
    { key: 'status', label: 'Status', sortable: true, width: 150, minWidth: 120 },
    { key: 'seo_score', label: 'SEO Score', sortable: true, width: 100, minWidth: 80 },
    { key: 'created_at', label: 'Created', sortable: true, width: 150, minWidth: 120 },
    { key: 'actions', label: 'Actions', sortable: false, width: 120, minWidth: 100 }
  ])
  const queryClient = useQueryClient()

  // Fetch content from API
  const { data: content = [], isLoading, error } = useQuery({
    queryKey: ['content'],
    queryFn: () => contentApi.list().then(res => res.data),
  })

  // Delete mutation
  const deleteMutation = useMutation({
    mutationFn: (id: number) => contentApi.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['content'] })
      notifications.show({
        title: 'Content Deleted',
        message: 'Content has been successfully deleted',
        color: 'green',
      })
    },
    onError: () => {
      notifications.show({
        title: 'Delete Failed',
        message: 'There was an error deleting the content',
        color: 'red',
      })
    },
  })

  // Sort and filter content
  const sortedAndFilteredContent = useMemo(() => {
    let filtered = content.filter((item: Content) => {
      if (statusFilter && item.status !== statusFilter) return false
      if (typeFilter && item.content_type !== typeFilter) return false
      if (search && !item.title.toLowerCase().includes(search.toLowerCase())) return false
      return true
    })

    // Sort the filtered content
    filtered.sort((a: Content, b: Content) => {
      let aValue: any = a[sortField as keyof Content]
      let bValue: any = b[sortField as keyof Content]

      // Handle special cases
      if (sortField === 'business') {
        aValue = a.business?.name || ''
        bValue = b.business?.name || ''
      } else if (sortField === 'seo_score') {
        aValue = a.seo_score || 0
        bValue = b.seo_score || 0
      } else if (sortField === 'created_at') {
        aValue = new Date(a.created_at).getTime()
        bValue = new Date(b.created_at).getTime()
      }

      // Convert to string for consistent comparison
      aValue = String(aValue).toLowerCase()
      bValue = String(bValue).toLowerCase()

      if (sortDirection === 'asc') {
        return aValue < bValue ? -1 : aValue > bValue ? 1 : 0
      } else {
        return aValue > bValue ? -1 : aValue < bValue ? 1 : 0
      }
    })

    return filtered
  }, [content, statusFilter, typeFilter, search, sortField, sortDirection])

  // Handle sorting
  const handleSort = (field: SortField) => {
    if (sortField === field) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc')
    } else {
      setSortField(field)
      setSortDirection('asc')
    }
  }

  // Handle column resize
  const handleColumnResize = (columnKey: string, newWidth: number) => {
    setColumns(prev => prev.map(col => 
      col.key === columnKey 
        ? { ...col, width: Math.max(newWidth, col.minWidth) }
        : col
    ))
  }

  const handleViewContent = (item: Content) => {
    setSelectedContent(item)
    openView()
  }

  const handleEditContent = (item: Content) => {
    setSelectedContent(item)
    openEdit()
  }

  const handleSaveEdit = async (title: string, content: string) => {
    if (!selectedContent) return
    
    try {
      // Update the content in the database
      await contentApi.update(selectedContent.id, {
        title,
        content_text: content
      })
      
      // Refresh the content list
      queryClient.invalidateQueries({ queryKey: ['content'] })
      
      notifications.show({
        title: 'Content Updated!',
        message: 'Your content has been successfully edited',
        color: 'green',
      })
    } catch (error) {
      notifications.show({
        title: 'Update Failed',
        message: 'There was an error updating the content',
        color: 'red',
      })
    }
  }

  const handleDeleteContent = (id: number) => {
    if (window.confirm('Are you sure you want to delete this content?')) {
      deleteMutation.mutate(id)
    }
  }

  const rows = sortedAndFilteredContent.map((item: Content) => (
    <Table.Tr key={item.id}>
      {columns.map((column, index) => (
        <Table.Td 
          key={`${item.id}-${column.key}`}
          style={{ 
            width: column.width,
            minWidth: column.minWidth,
            padding: '12px',
            borderRight: index < columns.length - 1 ? '1px solid #f1f3f4' : undefined
          }}
        >
          {column.key === 'title' && (
            <div>
              <Text fw={500} size="sm" style={{ 
                overflow: 'hidden', 
                textOverflow: 'ellipsis', 
                whiteSpace: 'nowrap',
                maxWidth: column.width - 24
              }}>
                {item.title}
              </Text>
              <Text size="xs" c="dimmed" style={{ 
                overflow: 'hidden', 
                textOverflow: 'ellipsis', 
                whiteSpace: 'nowrap',
                maxWidth: column.width - 24
              }}>
                {item.business?.name || 'Unknown Business'}
              </Text>
            </div>
          )}
          
          {column.key === 'content_type' && (
            <Badge size="sm" variant="light">
              {contentTypeLabels[item.content_type as keyof typeof contentTypeLabels]}
            </Badge>
          )}
          
          {column.key === 'status' && (
            <Badge 
              size="sm" 
              color={statusColors[item.status as keyof typeof statusColors]}
            >
              {item.status.replace('_', ' ')}
            </Badge>
          )}
          
          {column.key === 'seo_score' && (
            <Badge 
              size="sm" 
              color={item.seo_score && item.seo_score >= 80 ? 'green' : item.seo_score && item.seo_score >= 60 ? 'yellow' : item.seo_score ? 'red' : 'gray'}
              variant="light"
            >
              {item.seo_score ? `${item.seo_score}%` : 'N/A'}
            </Badge>
          )}
          
          {column.key === 'created_at' && (
            <Text size="sm">
              {new Date(item.created_at).toLocaleDateString()}
            </Text>
          )}
          
          {column.key === 'actions' && (
            <Group gap="xs">
              <ActionIcon 
                variant="subtle" 
                size="sm"
                onClick={() => handleViewContent(item)}
                title="View content"
              >
                <IconEye size={16} />
              </ActionIcon>
              <ActionIcon 
                variant="subtle" 
                size="sm"
                onClick={() => handleEditContent(item)}
                title="Edit content"
              >
                <IconEdit size={16} />
              </ActionIcon>
              <ActionIcon 
                variant="subtle" 
                size="sm" 
                color="red"
                onClick={() => handleDeleteContent(item.id)}
                loading={deleteMutation.isPending}
                title="Delete content"
              >
                <IconTrash size={16} />
              </ActionIcon>
            </Group>
          )}
        </Table.Td>
      ))}
    </Table.Tr>
  ))

  if (error) {
    return (
      <Stack gap="lg">
        <Text size="xl" fw={700}>Content Library</Text>
        <Card shadow="sm" padding="lg" radius="md" withBorder>
          <Text ta="center" c="red" py="xl">
            Error loading content. Please try again.
          </Text>
        </Card>
      </Stack>
    )
  }

  return (
    <Stack gap="lg">
      <Group justify="space-between">
        <Text size="xl" fw={700}>
          Content Library
        </Text>
        <Button 
          leftSection={<IconPlus size={16} />}
          onClick={() => navigate('/generate')}
        >
          Generate New Content
        </Button>
      </Group>

      <Card shadow="sm" padding="lg" radius="md" withBorder>
        <LoadingOverlay visible={isLoading} />
        <Group gap="md" mb="md">
          <TextInput
            placeholder="Search content..."
            leftSection={<IconSearch size={16} />}
            value={search}
            onChange={(e) => setSearch(e.currentTarget.value)}
            style={{ flex: 1 }}
          />
          <Select
            placeholder="Filter by status"
            data={[
              { value: '', label: 'All statuses' },
              { value: 'published', label: 'Published' },
              { value: 'pending_approval', label: 'Pending Approval' },
              { value: 'draft', label: 'Draft' },
            ]}
            value={statusFilter}
            onChange={setStatusFilter}
            clearable
          />
          <Select
            placeholder="Filter by type"
            data={[
              { value: '', label: 'All types' },
              { value: 'blog_post', label: 'Blog Post' },
              { value: 'linkedin_post', label: 'LinkedIn' },
              { value: 'twitter_post', label: 'Twitter' },
              { value: 'facebook_post', label: 'Facebook' },
              { value: 'instagram_post', label: 'Instagram' },
            ]}
            value={typeFilter}
            onChange={setTypeFilter}
            clearable
          />
        </Group>

        <Box style={{ overflow: 'auto' }}>
          <Table striped highlightOnHover style={{ minWidth: '800px' }}>
            <Table.Thead>
              <Table.Tr>
                {columns.map((column, index) => (
                  <Table.Th 
                    key={column.key}
                    style={{ 
                      width: column.width,
                      minWidth: column.minWidth,
                      position: 'relative',
                      padding: '8px 4px 8px 12px',
                      borderRight: index < columns.length - 1 ? '1px solid #e9ecef' : undefined
                    }}
                  >
                    <Group gap="xs" justify="space-between" wrap="nowrap">
                      {column.sortable ? (
                        <UnstyledButton
                          onClick={() => handleSort(column.key as SortField)}
                          style={{ flex: 1, display: 'flex', alignItems: 'center', gap: 4 }}
                        >
                          <Text size="sm" fw={500}>
                            {column.label}
                          </Text>
                          <Center>
                            {sortField === column.key ? (
                              sortDirection === 'desc' ? (
                                <IconChevronDown size={14} />
                              ) : (
                                <IconChevronUp size={14} />
                              )
                            ) : (
                              <IconSelector size={14} />
                            )}
                          </Center>
                        </UnstyledButton>
                      ) : (
                        <Text size="sm" fw={500}>
                          {column.label}
                        </Text>
                      )}
                      
                      {index < columns.length - 1 && (
                        <Box
                          style={{
                            position: 'absolute',
                            right: -2,
                            top: 0,
                            bottom: 0,
                            width: 4,
                            cursor: 'col-resize',
                            zIndex: 1,
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center'
                          }}
                          onMouseDown={(e) => {
                            const startX = e.clientX
                            const startWidth = column.width
                            
                            const handleMouseMove = (e: MouseEvent) => {
                              const newWidth = startWidth + (e.clientX - startX)
                              handleColumnResize(column.key, newWidth)
                            }
                            
                            const handleMouseUp = () => {
                              document.removeEventListener('mousemove', handleMouseMove)
                              document.removeEventListener('mouseup', handleMouseUp)
                              setResizing(null)
                            }
                            
                            setResizing(column.key)
                            document.addEventListener('mousemove', handleMouseMove)
                            document.addEventListener('mouseup', handleMouseUp)
                          }}
                        >
                          <IconGripVertical 
                            size={12} 
                            style={{ 
                              opacity: resizing === column.key ? 0.8 : 0.3,
                              transition: 'opacity 0.2s'
                            }} 
                          />
                        </Box>
                      )}
                    </Group>
                  </Table.Th>
                ))}
              </Table.Tr>
            </Table.Thead>
            <Table.Tbody>
              {rows.length > 0 ? rows : (
                <Table.Tr>
                  <Table.Td colSpan={columns.length}>
                    <Text ta="center" c="dimmed" py="xl">
                      No content found
                    </Text>
                  </Table.Td>
                </Table.Tr>
              )}
            </Table.Tbody>
          </Table>
        </Box>
      </Card>

      {/* View Content Modal */}
      <Modal
        opened={viewOpened}
        onClose={closeView}
        title="Content Details"
        size="xl"
        centered
        withCloseButton
        withinPortal={false}
        trapFocus
        lockScroll
        overlayProps={{ backgroundOpacity: 0.2, blur: 0 }}
        styles={{
          content: {
            zIndex: 10000,
            backgroundColor: 'white',
            border: '1px solid #e9ecef',
            boxShadow: '0 10px 40px rgba(0, 0, 0, 0.15)',
            borderRadius: '8px',
            margin: '0 auto',
          },
          overlay: {
            zIndex: 9999,
          },
          header: {
            backgroundColor: 'white',
            borderBottom: '1px solid #e9ecef',
            padding: '16px 24px',
            zIndex: 10001,
            position: 'relative',
          },
          body: {
            backgroundColor: 'white',
            padding: '24px',
            zIndex: 10001,
            position: 'relative',
          },
          inner: {
            zIndex: 10000,
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
          },
          root: {
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
          },
        }}
      >
        <div>
        
        {selectedContent && (
          <Stack gap="md">
            <div>
              <Text size="sm" fw={600} mb={5}>Title:</Text>
              <Text size="sm">{selectedContent.title}</Text>
            </div>
            
            <div>
              <Text size="sm" fw={600} mb={5}>Business:</Text>
              <Text size="sm">{selectedContent.business?.name || 'Unknown Business'}</Text>
            </div>
            
            <div>
              <Text size="sm" fw={600} mb={5}>Content Type:</Text>
              <Badge size="sm" variant="light">
                {contentTypeLabels[selectedContent.content_type as keyof typeof contentTypeLabels]}
              </Badge>
            </div>
            
            <div>
              <Text size="sm" fw={600} mb={5}>Status:</Text>
              <Badge 
                size="sm" 
                color={statusColors[selectedContent.status as keyof typeof statusColors]}
              >
                {selectedContent.status.replace('_', ' ')}
              </Badge>
            </div>
            
            {selectedContent.seo_score && (
              <div>
                <Text size="sm" fw={600} mb={5}>SEO Score:</Text>
                <Badge 
                  size="sm" 
                  color={selectedContent.seo_score >= 80 ? 'green' : selectedContent.seo_score >= 60 ? 'yellow' : 'red'}
                  variant="light"
                >
                  {selectedContent.seo_score}%
                </Badge>
              </div>
            )}
            
            {selectedContent.keywords && selectedContent.keywords.length > 0 && (
              <div>
                <Text size="sm" fw={600} mb={5}>Keywords:</Text>
                <Group gap="xs">
                  {selectedContent.keywords.map((keyword, index) => (
                    <Badge key={index} size="sm" variant="outline">
                      {keyword}
                    </Badge>
                  ))}
                </Group>
              </div>
            )}
            
            {selectedContent.meta_description && (
              <div>
                <Text size="sm" fw={600} mb={5}>Meta Description:</Text>
                <Text size="sm" c="dimmed">{selectedContent.meta_description}</Text>
              </div>
            )}
            
            <div>
              <Text size="sm" fw={600} mb={5}>Content:</Text>
              <Card shadow="xs" padding="sm" radius="sm" withBorder>
                <Text size="sm" style={{ whiteSpace: 'pre-wrap' }}>
                  {selectedContent.content_text}
                </Text>
              </Card>
            </div>
            
            <div>
              <Text size="sm" fw={600} mb={5}>Created:</Text>
              <Text size="sm">{new Date(selectedContent.created_at).toLocaleString()}</Text>
            </div>
          </Stack>
        )}
        </div>
      </Modal>

      {/* Edit Content Modal */}
      <EditContentModal
        opened={editOpened}
        onClose={closeEdit}
        title={selectedContent?.title || ''}
        content={selectedContent?.content_text || ''}
        onSave={handleSaveEdit}
      />
    </Stack>
  )
}